# Architecture

## Indexing path

The local indexing pipeline loads Markdown documentation, preserves page
metadata, splits pages into overlapping word chunks, and creates two searchable
representations.

The lexical representation is a TF-IDF sparse matrix. The semantic-style
representation applies Truncated SVD to the TF-IDF matrix to create dense LSA
vectors.

## Query path

A question is transformed using the same fitted vectorizer. Depending on the
selected strategy, retrieval uses lexical cosine similarity, dense LSA cosine
similarity, or a weighted combination of both.

Top-ranked chunks retain their original title, file name, and URL.

## Generation

The default generator is extractive. It ranks sentences from retrieved chunks
against the question and returns the best-supported sentence. This keeps the
repository runnable without an external LLM.

The generator is intentionally isolated from retrieval so an OpenAI, Anthropic,
local Hugging Face, or other LLM implementation can replace it later.

## Evaluation

The evaluation set is never indexed. Each QA record specifies an expected source
and answer facts. This makes retrieval changes measurable and reduces the risk of
evaluating the system only with hand-picked examples.
