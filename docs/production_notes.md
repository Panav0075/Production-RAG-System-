# Production Notes

This repository uses small local components so the full workflow can be run
without infrastructure or API credentials.

A larger deployment would normally separate ingestion, indexing, retrieval,
generation, and evaluation into independently observable components.

Important production additions include:

- scheduled and event-driven document ingestion
- content hashing and incremental re-indexing
- vector database persistence
- document and chunk version IDs
- tenant and permission filtering
- secret management
- prompt-injection handling
- PII controls
- request tracing
- retrieval latency dashboards
- LLM latency and token-cost tracking
- evaluation datasets versioned with releases
- online user-feedback signals
- canary testing before retrieval or prompt changes
- fallbacks for low-confidence retrieval
