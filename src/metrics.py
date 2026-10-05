import re
from collections import Counter


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())


def token_f1(prediction, expected):
    pred_tokens = normalize_text(prediction).split()
    expected_tokens = normalize_text(expected).split()

    if not pred_tokens or not expected_tokens:
        return float(pred_tokens == expected_tokens)

    common = Counter(pred_tokens) & Counter(expected_tokens)
    overlap = sum(common.values())

    if overlap == 0:
        return 0.0

    precision = overlap / len(pred_tokens)
    recall = overlap / len(expected_tokens)
    return 2 * precision * recall / (precision + recall)


def keyword_coverage(prediction, keywords):
    if not keywords:
        return 1.0
    normalized = normalize_text(prediction)
    matched = sum(normalize_text(keyword) in normalized for keyword in keywords)
    return matched / len(keywords)


def reciprocal_rank(retrieved, expected_source):
    for item in retrieved:
        if item["source"] == expected_source:
            return 1.0 / item["rank"]
    return 0.0


def hit_at_k(retrieved, expected_source, k):
    return float(any(item["source"] == expected_source for item in retrieved[:k]))
