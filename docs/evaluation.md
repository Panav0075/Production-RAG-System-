# Evaluation Design

The evaluation suite measures retrieval and answer behavior separately.

## Retrieval metrics

### Hit@1

The expected document is the first result.

### Hit@3

The expected document appears somewhere in the first three results.

### Mean Reciprocal Rank

MRR gives a score of 1 when the expected document is ranked first, 0.5 when it is
second, 0.333 when it is third, and so on.

## Answer metrics

### Token F1

Token F1 is a lightweight comparison between the generated sentence and the
reference answer.

### Keyword coverage

Some reference answers can be phrased in several valid ways. Each QA record
therefore contains important facts that should be present in a useful answer.

## What these metrics do not measure

Automatic metrics alone do not prove that a RAG system is production ready.
Human evaluation is still needed for faithfulness, completeness, ambiguity,
safety, and usefulness. Production systems should also measure latency, cost,
retrieval confidence, failures, and changes across index/model versions.
