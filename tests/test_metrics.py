from src.metrics import hit_at_k, keyword_coverage, reciprocal_rank, token_f1


def test_retrieval_metrics():
    results = [
        {"source": "wrong.md", "rank": 1},
        {"source": "right.md", "rank": 2},
    ]
    assert hit_at_k(results, "right.md", 1) == 0.0
    assert hit_at_k(results, "right.md", 2) == 1.0
    assert reciprocal_rank(results, "right.md") == 0.5


def test_answer_metrics():
    assert token_f1("The limit is 250 MB.", "The limit is 250 MB.") == 1.0
    assert keyword_coverage("The Pro limit is 250 MB.", ["Pro", "250 MB"]) == 1.0
