# Production RAG System with Retrieval Evaluation

A practical Retrieval-Augmented Generation (RAG) project focused on a question that matters in real applications:

**How do we know whether changing the retrieval strategy actually improves the answers?**

This repository implements an end-to-end RAG workflow using a small documentation-style knowledge base. It includes document ingestion, chunking, sparse and dense-style retrieval, hybrid ranking, answer generation, source citations, automated QA evaluation, and a comparison report across retrieval strategies.

The project is intentionally structured like an engineering repository rather than a single notebook.

> The included knowledge base and QA set are synthetic and were created for this portfolio project. No private company documents, customer data, or proprietary website content are included.

---

## What the system does

The pipeline:

1. Loads documentation pages from the local knowledge base.
2. Splits each page into searchable chunks.
3. Builds lexical and semantic-style representations.
4. Retrieves relevant chunks for a user question.
5. Supports multiple retrieval strategies.
6. Generates a grounded answer from retrieved context.
7. Returns the source pages used for the answer.
8. Evaluates retrieval quality against a labeled QA set.
9. Produces a comparison table showing which retrieval strategy performs best.

The repository can run locally without requiring a paid API key. An extractive answer generator is included so the complete evaluation pipeline remains reproducible.

---

## Architecture

```text
                    Documentation / Site Pages
                              |
                              v
                     +------------------+
                     | Document Loader  |
                     +--------+---------+
                              |
                              v
                     +------------------+
                     | Text Chunking    |
                     | metadata + IDs   |
                     +--------+---------+
                              |
                    +---------+----------+
                    |                    |
                    v                    v
            +---------------+    +---------------+
            | TF-IDF Index  |    | LSA Embedding |
            | lexical       |    | semantic      |
            +-------+-------+    +-------+-------+
                    |                    |
                    +---------+----------+
                              |
                    +---------v----------+
                    | Retrieval Strategy |
                    | lexical / semantic |
                    | hybrid             |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    | Top-K Context      |
                    | + source metadata  |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    | Grounded Answer    |
                    | + citations        |
                    +---------+----------+
                              |
                              v
                    +--------------------+
                    | QA Evaluation      |
                    | Hit@K / MRR / F1   |
                    +---------+----------+
                              |
                              v
                    Retrieval Comparison
```

---

## Retrieval strategies

### 1. Lexical retrieval

Uses TF-IDF vectors and cosine similarity.

This works well when the question contains the same terminology used in the documentation.

### 2. Semantic retrieval

Uses Latent Semantic Analysis (LSA) over the TF-IDF matrix. Truncated SVD creates dense document representations that can retrieve related text even when the exact word overlap is lower.

The implementation is deliberately local so the project is reproducible without downloading a large embedding model.

### 3. Hybrid retrieval

Combines normalized lexical and semantic scores:

```text
hybrid_score = alpha * lexical_score + (1 - alpha) * semantic_score
```

The default configuration uses `alpha = 0.55`.

---

## Knowledge base

The sample site contains documentation pages covering:

- authentication
- API rate limits
- webhooks
- billing
- data retention
- account security
- file uploads
- team permissions

Each page contains metadata such as:

```json
{
  "source": "authentication.md",
  "title": "Authentication",
  "url": "https://docs.example.local/authentication"
}
```

The URLs are intentionally illustrative local documentation URLs. They are included to demonstrate source tracking and citation behavior.

---

## Example

Question:

```text
How long are audit logs retained on the Pro plan?
```

Retrieved source:

```text
Data Retention
https://docs.example.local/data-retention
```

Generated answer:

```text
Audit logs are retained for 180 days on the Pro plan.
```

The answer object also contains the retrieved sources and their scores.

---

## Evaluation dataset

`data/evaluation/qa_pairs.json` contains labeled questions with:

- question
- expected answer
- expected source
- relevant keywords

Example:

```json
{
  "question": "What happens after five failed login attempts?",
  "expected_answer": "The account is locked for 15 minutes.",
  "expected_source": "account-security.md",
  "keywords": ["locked", "15 minutes"]
}
```

This lets retrieval and answer quality be evaluated automatically instead of judging a few examples manually.

---

## Evaluation metrics

### Hit@K

Checks whether the expected source appears anywhere in the top-K retrieved results.

### Mean Reciprocal Rank (MRR)

Rewards systems that place the correct source closer to rank 1.

### Answer token F1

Compares normalized tokens in the generated answer with the expected answer.

### Keyword coverage

Checks how many required facts from the labeled QA record appear in the generated answer.

---

## Retrieval comparison

The project generates this table automatically by running:

```bash
python -m src.evaluate
```

A completed evaluation report is also included in `reports/retrieval_evaluation.md`.

| Strategy | Hit@1 | Hit@3 | MRR | Answer F1 | Keyword Coverage |
|---|---:|---:|---:|---:|---:|
| Lexical | 1.000 | 1.000 | 1.000 | 0.443 | 0.583 |
| Semantic | 1.000 | 1.000 | 1.000 | 0.443 | 0.583 |
| Hybrid | 1.000 | 1.000 | 1.000 | 0.443 | 0.583 |

These values are from the included 16-question QA benchmark. They can be reproduced with `python -m src.evaluate`. The benchmark is intentionally small, so perfect source retrieval should be treated as a pipeline check rather than a claim about production accuracy.

---

## Repository structure

```text
production-rag-evaluation/
├── README.md
├── requirements.txt
├── config.yaml
├── .gitignore
├── Makefile
│
├── src/
│   ├── __init__.py
│   ├── schemas.py
│   ├── loader.py
│   ├── chunking.py
│   ├── index.py
│   ├── retriever.py
│   ├── generator.py
│   ├── rag.py
│   ├── metrics.py
│   ├── evaluate.py
│   └── demo.py
│
├── data/
│   ├── source_docs/
│   │   ├── authentication.md
│   │   ├── rate-limits.md
│   │   ├── webhooks.md
│   │   ├── billing.md
│   │   ├── data-retention.md
│   │   ├── account-security.md
│   │   ├── file-uploads.md
│   │   └── team-permissions.md
│   └── evaluation/
│       └── qa_pairs.json
│
├── tests/
│   ├── test_chunking.py
│   ├── test_retriever.py
│   └── test_metrics.py
│
├── reports/
│   ├── retrieval_evaluation.md
│   └── evaluation_results.json
│
├── docs/
│   ├── architecture.md
│   ├── evaluation.md
│   └── production_notes.md
│
└── .github/
    └── workflows/
        └── tests.yml
```

---

## Run locally

### 1. Create an environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Ask a question

```bash
python -m src.demo "How do I verify a webhook request?"
```

You can choose a strategy:

```bash
python -m src.demo "How do I verify a webhook request?" --strategy hybrid
```

Supported values:

```text
lexical
semantic
hybrid
```

### 4. Run the evaluation

```bash
python -m src.evaluate
```

### 5. Run tests

```bash
pytest -q
```

---

## Example programmatic usage

```python
from src.rag import RAGSystem

rag = RAGSystem.from_config("config.yaml")

result = rag.ask(
    "What is the maximum upload size on the Pro plan?",
    strategy="hybrid",
)

print(result["answer"])

for source in result["sources"]:
    print(source["title"], source["url"])
```

---

## Why evaluation is part of the repository

A RAG demo can look good even when retrieval is unreliable.

For example, an answer may sound correct while the retriever is consistently returning the wrong document. That becomes difficult to notice when testing only a few questions by hand.

This project separates two questions:

1. **Did we retrieve the right information?**
2. **Did the final answer contain the expected facts?**

That makes it possible to compare retrieval changes with measurable results.

---

## Production considerations

The local implementation keeps the project easy to run, but the architecture can be extended to production services.

Typical replacements would be:

```text
Local Markdown loader
        -> web crawler / object storage / document pipeline

TF-IDF + LSA
        -> embedding model

In-memory matrices
        -> vector database

Extractive generator
        -> hosted or local LLM

Local evaluation JSON
        -> evaluation service / experiment tracking
```

A production deployment would also need:

- incremental indexing
- document versioning
- metadata filtering
- access-control-aware retrieval
- prompt-injection defenses
- PII handling
- observability and tracing
- latency monitoring
- model and retrieval version tracking
- offline and online evaluation
- fallback behavior when retrieval confidence is low

---

## Design choices

### Why include an extractive generator?

The repository should work without requiring an API key. The included generator selects the most relevant sentence from retrieved context. An LLM can later replace this component without changing the retrieval evaluation design.

### Why track source URLs?

A useful RAG answer should be traceable. Every chunk keeps its original document metadata so the final response can show where its information came from.

### Why compare several retrievers?

There is no universally best retrieval strategy. The right approach depends on the documents, vocabulary, questions, chunking method, and evaluation target.

### Why keep the QA set separate?

The source documents are what the RAG system searches. The QA file is an evaluation artifact and is never added to the retrieval index.

---

## Tech stack

**Python · scikit-learn · NumPy · PyYAML · Pytest**

Main concepts demonstrated:

**RAG · information retrieval · TF-IDF · semantic search · hybrid retrieval · source attribution · QA evaluation · MRR · Hit@K · answer evaluation**

---

## Future improvements

- replace LSA with sentence-transformer embeddings
- add FAISS, Pinecone, Weaviate, or Milvus
- add reranking with a cross-encoder
- integrate an LLM answer generator
- add RAGAS-style faithfulness metrics
- evaluate different chunk sizes and overlaps
- add query rewriting
- add metadata filters
- add FastAPI endpoints
- add Docker support
- add MLflow or experiment tracking
- evaluate retrieval latency and cost
