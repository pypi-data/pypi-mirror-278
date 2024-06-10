import itertools
import json
import random
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Union

import numpy as np
from rich.console import Console
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import NMF, MiniBatchNMF
from sklearn.decomposition._nmf import (_initialize_nmf,
                                        _update_coordinate_descent)
from sklearn.exceptions import NotFittedError
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.utils import check_array

from turftopic.base import ContextualModel, Encoder
from turftopic.data import TopicData
from turftopic.dynamic import DynamicTopicModel, bin_timestamps
from turftopic.vectorizer import default_vectorizer


def fit_timeslice(
    X,
    W,
    H,
    tol=1e-4,
    max_iter=200,
    l1_reg_W=0,
    l1_reg_H=0,
    l2_reg_W=0,
    l2_reg_H=0,
    verbose=0,
    shuffle=False,
    random_state=None,
):
    """Fits topic_term_matrix based on a precomputed document_topic_matrix.
    This is used to get temporal components in dynamic KeyNMF.
    """
    Ht = check_array(H.T, order="C")
    if random_state is None:
        rng = np.random.mtrand._rand
    else:
        rng = np.random.RandomState(random_state)
    for n_iter in range(1, max_iter + 1):
        violation = 0.0
        violation += _update_coordinate_descent(
            X.T, Ht, W, l1_reg_H, l2_reg_H, shuffle, rng
        )
        if n_iter == 1:
            violation_init = violation
        if violation_init == 0:
            break
        if verbose:
            print("violation:", violation / violation_init)
        if violation / violation_init <= tol:
            if verbose:
                print("Converged at iteration", n_iter + 1)
            break
    return W, Ht.T, n_iter


def batched(iterable, n: int) -> Iterable[List[str]]:
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := list(itertools.islice(it, n)):
        yield batch


def serialize_keywords(keywords: Dict[str, float]) -> str:
    return json.dumps(
        {word: str(importance) for word, importance in keywords.items()}
    )


def deserialize_keywords(s: str) -> Dict[str, float]:
    obj = json.loads(s)
    return {word: float(importance) for word, importance in obj.items()}


class KeywordIterator:
    def __init__(self, file: str):
        self.file = file

    def __iter__(self) -> Iterable[Dict[str, float]]:
        with open(self.file) as in_file:
            for line in in_file:
                yield deserialize_keywords(line.strip())


class KeyNMF(ContextualModel, DynamicTopicModel):
    """Extracts keywords from documents based on semantic similarity of
    term encodings to document encodings.
    Topics are then extracted with non-negative matrix factorization from
    keywords' proximity to documents.

    ```python
    from turftopic import KeyNMF

    corpus: list[str] = ["some text", "more text", ...]

    model = KeyNMF(10, top_n=10).fit(corpus)
    model.print_topics()
    ```

    Parameters
    ----------
    n_components: int
        Number of topics.
    encoder: str or SentenceTransformer
        Model to encode documents/terms, all-MiniLM-L6-v2 is the default.
    vectorizer: CountVectorizer, default None
        Vectorizer used for term extraction.
        Can be used to prune or filter the vocabulary.
    top_n: int, default 25
        Number of keywords to extract for each document.
    keyword_scope: str, default 'document'
        Specifies whether keyword extraction for each document
        is performed on the whole vocabulary ('corpus') or only
        using words that are included in the document ('document').
        Setting this to 'corpus' allows for multilingual topics.
    random_state: int, default None
        Random state to use so that results are exactly reproducible.
    """

    def __init__(
        self,
        n_components: int,
        encoder: Union[
            Encoder, str
        ] = "sentence-transformers/all-MiniLM-L6-v2",
        vectorizer: Optional[CountVectorizer] = None,
        top_n: int = 25,
        keyword_scope: str = "document",
        random_state: Optional[int] = None,
    ):
        self.random_state = random_state
        if keyword_scope not in ["document", "corpus"]:
            raise ValueError("keyword_scope must be 'document' or 'corpus'")
        self.n_components = n_components
        self.top_n = top_n
        self.encoder = encoder
        if isinstance(encoder, str):
            self.encoder_ = SentenceTransformer(encoder)
        else:
            self.encoder_ = encoder
        if vectorizer is None:
            self.vectorizer = default_vectorizer()
        else:
            self.vectorizer = vectorizer
        self.dict_vectorizer_ = DictVectorizer()
        self.nmf_ = NMF(n_components, random_state=self.random_state)
        self.keyword_scope = keyword_scope

    def extract_keywords(
        self,
        batch_or_document: Union[str, List[str]],
        embeddings: Optional[np.ndarray] = None,
    ) -> List[Dict[str, float]]:
        if isinstance(batch_or_document, str):
            batch_or_document = [batch_or_document]
        if embeddings is None:
            embeddings = self.encoder_.encode(batch_or_document)
        keywords = []
        total = embeddings.shape[0]
        document_term_matrix = self.vectorizer.transform(batch_or_document)
        for i in range(total):
            terms = document_term_matrix[i, :].todense()
            embedding = embeddings[i].reshape(1, -1)
            if self.keyword_scope == "document":
                mask = terms > 0
            else:
                tot_freq = document_term_matrix.sum(axis=0)
                mask = tot_freq != 0
            if not np.any(mask):
                keywords.append(dict())
                continue
            important_terms = np.squeeze(np.asarray(mask))
            word_embeddings = self.vocab_embeddings[important_terms]
            sim = cosine_similarity(embedding, word_embeddings)
            sim = np.ravel(sim)
            kth = min(self.top_n, len(sim) - 1)
            top = np.argpartition(-sim, kth)[:kth]
            top_words = self.vectorizer.get_feature_names_out()[
                important_terms
            ][top]
            top_sims = sim[top]
            keywords.append(dict(zip(top_words, top_sims)))
        return keywords

    def learn_vocabulary(self, document_stream: Iterable[str]):
        self.vectorizer.fit(document_stream)
        self.vocab_embeddings = self.encoder_.encode(
            self.vectorizer.get_feature_names_out()
        )

    def cache_keywords(
        self,
        document_stream: Iterable[str],
        keyword_file: str = "./__keywords.jsonl",
        batch_size: int = 500,
    ):
        with open(keyword_file, "w") as out_file:
            for document_batch in batched(document_stream, batch_size):
                keywords = self.extract_keywords(document_batch)
                serialized = "\n".join(
                    [serialize_keywords(k) for k in keywords]
                )
                out_file.write(serialized + "\n")

    def minibatch_train(
        self,
        keywords: Iterable[Dict[str, float]],
        max_epochs: int = 50,
        batch_size: int = 500,
        console=None,
    ):
        self.dict_vectorizer_.fit(keywords)
        self.nmf_ = MiniBatchNMF(
            self.n_components, random_state=self.random_state
        )
        epoch_costs = []
        for i_epoch in range(max_epochs):
            epoch_cost = 0
            entry_batches = batched(keywords, batch_size)
            for i_batch, batch in enumerate(entry_batches):
                random.shuffle(batch)
                dtm = self.dict_vectorizer_.transform(batch)
                dtm[dtm < 0] = 0  # type: ignore
                self.nmf_.partial_fit(dtm)
                batch_cost = self.nmf_._minibatch_step(
                    dtm, None, self.nmf_.components_, update_H=False
                )
                epoch_cost += batch_cost
            epoch_costs.append(epoch_cost)
            if (i_epoch > 5) and (
                epoch_costs[-1] >= epoch_costs[max(0, i_epoch - 5)]
            ):
                if console is not None:
                    console.log(
                        f"Converged after {i_epoch} epochs, early stopping."
                    )
                break
        self.components_ = self.nmf_.components_

    def big_fit(
        self,
        document_stream: Iterable[str],
        keyword_file: str = "./__keywords.jsonl",
        batch_size: int = 500,
        max_epochs: int = 100,
    ):
        """Fit KeyNMF on very large datasets, that cannot fit in memory.
        Internally uses minibatch NMF.
        The stream of documents has to be a reusable iterable,
        as multiple passes are needed over the corpus to
        learn the vocabulary and then fit the model.
        """
        console = Console()
        with console.status("Fitting model") as status:
            status.update("Learning vocabulary.")
            self.learn_vocabulary(document_stream)
            console.log("Vocabulary learnt.")
            status.update("Extracting keywords.")
            self.cache_keywords(document_stream, keyword_file, batch_size)
            console.log("Keywords extracted.")
            keywords = KeywordIterator(keyword_file)
            status.update("Fitting NMF.")
            self.minibatch_train(
                keywords, max_epochs, batch_size, console=console
            )  # type: ignore
            console.log("NMF fitted.")
        return self

    def fit_transform(
        self, raw_documents, y=None, embeddings: Optional[np.ndarray] = None
    ) -> np.ndarray:
        topic_data = self.prepare_topic_data(raw_documents, embeddings)
        return topic_data["document_topic_matrix"]

    def get_vocab(self) -> np.ndarray:
        return self.dict_vectorizer_.get_feature_names_out()

    def transform(
        self, raw_documents, embeddings: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Infers topic importances for new documents based on a fitted model.

        Parameters
        ----------
        raw_documents: iterable of str
            Documents to fit the model on.
        embeddings: ndarray of shape (n_documents, n_dimensions), optional
            Precomputed document encodings.

        Returns
        -------
        ndarray of shape (n_dimensions, n_topics)
            Document-topic matrix.
        """
        if embeddings is None:
            embeddings = self.encode_documents(raw_documents)
        keywords = self.extract_keywords(raw_documents, embeddings)
        representations = self.dict_vectorizer_.transform(keywords)
        representations[representations < 0] = 0
        return self.nmf_.transform(representations)

    def prepare_topic_data(
        self,
        corpus: List[str],
        embeddings: Optional[np.ndarray] = None,
    ) -> TopicData:
        console = Console()
        with console.status("Running KeyNMF") as status:
            if embeddings is None:
                status.update("Encoding documents")
                embeddings = self.encode_documents(corpus)
                console.log("Documents encoded.")
            if getattr(self, "components_", None) is None:
                status.update("Learning Vocabulary.")
                self.learn_vocabulary(corpus)
            status.update("Extracting keywords")
            keywords = self.extract_keywords(corpus, embeddings=embeddings)
            console.log("Keyword extraction done.")
            status.update("Decomposing with NMF")
            try:
                dtm = self.dict_vectorizer_.transform(keywords)
            except (NotFittedError, AttributeError):
                dtm = self.dict_vectorizer_.fit_transform(keywords)
            dtm[dtm < 0] = 0  # type: ignore
            try:
                doc_topic_matrix = self.nmf_.transform(dtm)
            except (NotFittedError, AttributeError):
                doc_topic_matrix = self.nmf_.fit_transform(dtm)
                self.components_ = self.nmf_.components_
            console.log("Model fitting done.")
        res: TopicData = {
            "corpus": corpus,
            "document_term_matrix": dtm,
            "vocab": self.get_vocab(),
            "document_topic_matrix": doc_topic_matrix,
            "document_representation": embeddings,
            "topic_term_matrix": self.components_,  # type: ignore
            "transform": getattr(self, "transform", None),
            "topic_names": self.topic_names,
        }
        return res

    def fit_transform_dynamic(
        self,
        raw_documents,
        timestamps: list[datetime],
        embeddings: Optional[np.ndarray] = None,
        bins: Union[int, list[datetime]] = 10,
    ) -> np.ndarray:
        time_labels, self.time_bin_edges = bin_timestamps(timestamps, bins)
        topic_data = self.prepare_topic_data(
            raw_documents, embeddings=embeddings
        )
        n_bins = len(self.time_bin_edges) + 1
        n_comp, n_vocab = self.components_.shape
        self.temporal_components_ = np.zeros((n_bins, n_comp, n_vocab))
        self.temporal_importance_ = np.zeros((n_bins, n_comp))
        for label in np.unique(time_labels):
            idx = np.nonzero(time_labels == label)
            X = topic_data["document_term_matrix"][idx]
            W = topic_data["document_topic_matrix"][idx]
            _, H = _initialize_nmf(
                X, self.components_.shape[0], random_state=self.random_state
            )
            _, H, _ = fit_timeslice(X, W, H, random_state=self.random_state)
            self.temporal_components_[label] = H
            topic_importances = np.squeeze(np.asarray(W.sum(axis=0)))
            topic_importances = topic_importances / topic_importances.sum()
            self.temporal_importance_[label] = topic_importances
        return topic_data["document_topic_matrix"]
