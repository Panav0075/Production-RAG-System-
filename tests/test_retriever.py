from src.rag import RAGSystem


def test_hybrid_retrieval_returns_expected_security_source():
    rag = RAGSystem.from_config("config.yaml")
    result = rag.ask(
        "What happens after five failed password attempts?",
        strategy="hybrid",
    )
    assert result["sources"][0]["source"] == "account-security.md"


def test_webhook_query_returns_source_metadata():
    rag = RAGSystem.from_config("config.yaml")
    result = rag.ask("How do I verify a webhook request?", strategy="hybrid")
    sources = [item["source"] for item in result["sources"]]
    assert "webhooks.md" in sources
    assert result["sources"][0]["url"].startswith("https://")
