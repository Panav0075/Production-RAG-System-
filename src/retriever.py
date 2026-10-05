import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def _normalize_scores(scores):
    scores = np.asarray(scores, dtype=float)
    minimum = scores.min()
    maximum = scores.max()
    if maximum - minimum < 1e-12:
        return np.zeros_like(scores)
    return (scores - minimum) / (maximum - minimum)


class Retriever:
    def __init__(self, index, hybrid_alpha=0.55):
        self.index = index
        self.hybrid_alpha = hybrid_alpha

    def scores(self, query, strategy="hybrid"):
        lexical_query = self.index.lexical_query(query)
        lexical = cosine_similarity(
            lexical_query,
            self.index.lexical_matrix,
        ).ravel()

        if self.index.semantic_matrix is None:
            semantic = lexical.copy()
        else:
            semantic_query = self.index.semantic_query(query)
            semantic = cosine_similarity(
                semantic_query,
                self.index.semantic_matrix,
            ).ravel()

        if strategy == "lexical":
            return lexical
        if strategy == "semantic":
            return semantic
        if strategy == "hybrid":
            return (
                self.hybrid_alpha * _normalize_scores(lexical)
                + (1.0 - self.hybrid_alpha) * _normalize_scores(semantic)
            )

        raise ValueError("strategy must be lexical, semantic, or hybrid")

    def retrieve(self, query, strategy="hybrid", top_k=3):
        scores = self.scores(query, strategy)
        order = np.argsort(scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(order, start=1):
            chunk = self.index.chunks[int(idx)]
            item = chunk.to_dict()
            item["rank"] = rank
            item["score"] = round(float(scores[int(idx)]), 6)
            results.append(item)
        return results
