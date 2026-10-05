import yaml

from .chunking import chunk_documents
from .generator import ExtractiveAnswerGenerator
from .index import RetrievalIndex
from .loader import load_documents
from .retriever import Retriever


class RAGSystem:
    def __init__(self, retriever, generator, top_k=3):
        self.retriever = retriever
        self.generator = generator
        self.top_k = top_k

    @classmethod
    def from_config(cls, config_path="config.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        documents = load_documents(cfg["documents"]["path"])
        chunks = chunk_documents(
            documents,
            chunk_size_words=cfg["retrieval"]["chunk_size_words"],
            overlap_words=cfg["retrieval"]["chunk_overlap_words"],
        )

        index = RetrievalIndex(
            chunks,
            semantic_dimensions=cfg["retrieval"]["semantic_dimensions"],
            random_state=cfg["retrieval"]["random_state"],
        )
        retriever = Retriever(
            index,
            hybrid_alpha=cfg["retrieval"]["hybrid_alpha"],
        )
        return cls(
            retriever,
            ExtractiveAnswerGenerator(),
            top_k=cfg["retrieval"]["top_k"],
        )

    def ask(self, question, strategy="hybrid"):
        retrieved = self.retriever.retrieve(
            question,
            strategy=strategy,
            top_k=self.top_k,
        )
        generated = self.generator.generate(question, retrieved)

        seen = set()
        sources = []
        for item in retrieved:
            key = item["source"]
            if key not in seen:
                seen.add(key)
                sources.append(
                    {
                        "title": item["title"],
                        "source": item["source"],
                        "url": item["url"],
                        "rank": item["rank"],
                        "score": item["score"],
                    }
                )

        return {
            "question": question,
            "strategy": strategy,
            "answer": generated["answer"],
            "answer_source": generated["source"],
            "sources": sources,
            "retrieved_chunks": retrieved,
        }
