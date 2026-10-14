# Hearth Orchestrator — AI Agent Systems Proof of Work

A focused portfolio for applied AI / agent-platform engineering: durable execution, source-grounded review, measurable routing, and explicit human/action boundaries.

> Status: active build. Evidence is labeled by where it was produced; results are not promoted to stronger claims than the test actually supports.

## Why this project

Current agent-platform roles increasingly expect more than prompt demos. They ask for durable execution, tool orchestration, routing, evaluation, observability, failure recovery, approval boundaries, and production-oriented backend judgment.

Hearth Orchestrator turns those requirements into one inspectable project with three case studies sharing the same runtime concepts.

## Case studies

### 1. Commit Reliability Lab

**Question:** Can an agent workflow survive duplicate delivery, overlapping writers, stale state, and interruption around commit without silently losing an authorized operation?

Current verified local/Drive evidence includes:

- a reproducible preflight + unconditional-write lost-update counterexample;
- a single-host Linux commit gateway using one persistent advisory writer lock;
- request-id binding and idempotent replay;
- stale revision rejection through the preserved Hearth state engine;
- atomic snapshot replacement with `fsync` of file and directory;
- corrupt-store fail-closed behavior;
- process/crash recovery tests.

Important boundary: this is a **local fixture adapter**, not a distributed lock service, a Google Drive transaction protocol, or proof of exactly-once external side effects.

### 2. Source-Grounded Change Review

**Question:** Can the workflow produce useful engineering findings while preserving evidence identity and abstaining when support is missing or disputed?

Target behavior:

- versioned citations and content digests;
- supported / disputed / unresolved findings;
- contradiction detection;
- prompt-injection separation between retrieved text and control instructions;
- human adjudication for ambiguous semantic cases;
- replayable review receipts.

### 3. Evidence-Backed Router

**Question:** When should a task use deterministic rules, retrieval, a model/tool step, clarification, or human review?

The next implementation milestone is a bounded router that records:

- route decision and reason;
- work / tool-call caps;
- clarification and human-review escalation;
- replay identity;
- outcome, latency, and quality fields for fixed-workflow comparison.

The router is evaluated against a simpler fixed workflow rather than assuming that more agent autonomy is better.

## Engineering principles

- Models may propose actions; deterministic code and authenticated approval decide what executes.
- Every run ends in an explicit state: success, failure, rejection, cancellation, or awaiting approval.
- Retries, loops, timeouts, and work budgets are bounded and observable.
- Approval binds to an exact action and input version.
- Evidence identity survives handoffs.
- Local tests, simulations, live integration tests, and inherited receipts are labeled separately.
- A hash proves byte identity under stated assumptions; it does not prove semantic truth.

## Portfolio roadmap

1. Publish the Commit Reliability Lab source and deterministic tests.
2. Publish the source-grounded review fixture set and evaluation rubric.
3. Implement the evidence-backed router and six-case fixed-workflow comparison.
4. Add GitHub Actions for reproducible tests on Linux/Python 3.12.
5. Add a small read-only trace viewer.
6. Only after the above is stable, consider live adapters (Drive/MCP/provider APIs) and multi-worker deployment.

## Interview discussion prompts this repo is designed to support

- Why is check-then-write not a compare-and-swap?
- What does idempotency guarantee, and what does it not guarantee?
- Where should an LLM stop and deterministic policy begin?
- How do you evaluate an agent by environment state rather than prose alone?
- When does a router outperform a fixed workflow enough to justify its complexity?
- How do failure recovery, auditability, cost, and latency change the design?

## Authorship note

This portfolio is being built by Philip Cervantes Jr. with AI-assisted implementation and review. AI-generated code is treated as code that must be understood, tested, modified, and defended—not as evidence of independent prior employment experience.
