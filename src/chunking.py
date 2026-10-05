from typing import Iterable, List

from .schemas import Chunk, Document


def chunk_document(
    document: Document,
    chunk_size_words: int = 95,
    overlap_words: int = 20,
) -> List[Chunk]:
    if chunk_size_words <= 0:
        raise ValueError("chunk_size_words must be positive")
    if overlap_words < 0 or overlap_words >= chunk_size_words:
        raise ValueError("overlap_words must be >= 0 and smaller than chunk_size_words")

    words = document.text.split()
    if not words:
        return []

    step = chunk_size_words - overlap_words
    chunks = []

    for chunk_index, start in enumerate(range(0, len(words), step)):
        window = words[start : start + chunk_size_words]
        if not window:
            break

        chunks.append(
            Chunk(
                chunk_id=f"{document.document_id}:{chunk_index}",
                document_id=document.document_id,
                title=document.title,
                source=document.source,
                url=document.url,
                text=" ".join(window),
                chunk_index=chunk_index,
            )
        )

        if start + chunk_size_words >= len(words):
            break

    return chunks


def chunk_documents(
    documents: Iterable[Document],
    chunk_size_words: int = 95,
    overlap_words: int = 20,
) -> List[Chunk]:
    chunks = []
    for document in documents:
        chunks.extend(
            chunk_document(
                document,
                chunk_size_words=chunk_size_words,
                overlap_words=overlap_words,
            )
        )
    return chunks
