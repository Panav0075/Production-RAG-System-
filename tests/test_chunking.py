from src.chunking import chunk_document
from src.schemas import Document


def test_chunking_keeps_metadata():
    doc = Document(
        document_id="demo",
        title="Demo",
        source="demo.md",
        url="https://example.local/demo",
        text=" ".join(f"word{i}" for i in range(120)),
    )
    chunks = chunk_document(doc, chunk_size_words=50, overlap_words=10)
    assert len(chunks) == 3
    assert chunks[0].source == "demo.md"
    assert chunks[0].url == "https://example.local/demo"
    assert chunks[1].text.split()[0] == "word40"
