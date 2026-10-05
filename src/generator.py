import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


class ExtractiveAnswerGenerator:
    """Local answer generator used so the repository works without an LLM API."""

    def generate(self, question, retrieved_chunks):
        candidates = []

        # Generate from the highest-ranked evidence. This keeps the answer
        # grounded in the source selected by retrieval instead of allowing a
        # lower-ranked chunk with incidental word overlap to dominate.
        evidence = retrieved_chunks[:1]
        for result in evidence:
            for sentence in SENTENCE_SPLIT.split(result["text"]):
                sentence = sentence.strip()
                if len(sentence.split()) >= 4:
                    candidates.append((sentence, result))

        if not candidates:
            return {
                "answer": "I could not find enough information in the indexed documents.",
                "source": None,
            }

        sentences = [item[0] for item in candidates]
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        matrix = vectorizer.fit_transform([question] + sentences)
        scores = cosine_similarity(matrix[0:1], matrix[1:]).ravel()
        best_idx = int(scores.argmax())

        sentence, source = candidates[best_idx]
        return {
            "answer": sentence,
            "source": {
                "title": source["title"],
                "source": source["source"],
                "url": source["url"],
            },
        }
