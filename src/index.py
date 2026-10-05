import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


class RetrievalIndex:
    def __init__(self, chunks, semantic_dimensions=24, random_state=42):
        if not chunks:
            raise ValueError("Cannot build an index without chunks")

        self.chunks = chunks
        corpus = [chunk.text for chunk in chunks]

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
        )
        self.lexical_matrix = self.vectorizer.fit_transform(corpus)

        max_components = min(
            semantic_dimensions,
            max(1, self.lexical_matrix.shape[0] - 1),
            max(1, self.lexical_matrix.shape[1] - 1),
        )

        self.svd = None
        self.semantic_matrix = None

        if max_components >= 2:
            self.svd = TruncatedSVD(
                n_components=max_components,
                random_state=random_state,
            )
            dense = self.svd.fit_transform(self.lexical_matrix)
            self.semantic_matrix = normalize(dense)

    def lexical_query(self, query):
        return self.vectorizer.transform([query])

    def semantic_query(self, query):
        lexical = self.lexical_query(query)
        if self.svd is None:
            return None
        return normalize(self.svd.transform(lexical))
