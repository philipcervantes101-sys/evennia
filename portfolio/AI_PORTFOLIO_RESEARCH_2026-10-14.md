# AI Agent Systems Portfolio — Role Signal Research

Date: 2026-10-14

This note records the current hiring signal used to prioritize the Hearth Orchestrator portfolio. It is a purposive sample of current role descriptions, not a statistical labor-market survey.

## Current role signals

### OpenAI — Software Engineer, Agent Infrastructure

Role page: https://openai.com/careers/software-engineer-agent-infrastructure-san-francisco/

Signals relevant to the portfolio:

- infrastructure for training and deployment of useful agents;
- environments where agents execute code and interact with software;
- production execution platforms for agentic products;
- orchestration and high-scale infrastructure;
- APIs and operational engineering.

### OpenAI — Software Engineer, API Agents

Role page: https://openai.com/careers/software-engineer-api-agents-san-francisco/

Signals relevant to the portfolio:

- shared agent harness and backend infrastructure;
- long-running workflows;
- search and connected context;
- tool execution, delegation, subagents, multi-agent orchestration;
- secure execution, identity and permissions;
- observability, evaluations, reliability, cost and latency efficiency.

### OpenAI — AI Systems Engineer, Codex Agents

Role page: https://openai.com/careers/ai-systems-engineer-codex-agents-san-francisco/

Signals relevant to the portfolio:

- core agent harness and execution loop;
- safe tool use and code execution;
- orchestration, state, workflow infrastructure, sandboxing;
- evals, experiments, ablations, debugging;
- reliability, latency, cost, quality, and observability.

### OpenAI — Software Engineer, Cloud Agents

Role page: https://openai.com/careers/software-engineer-cloud-agents-san-francisco/

Signals relevant to the portfolio:

- infrastructure for long-running cloud agents;
- orchestration, isolation, connectivity, secrets and identity;
- observability, reliability, and cost controls;
- backend and distributed-systems judgment.

### OpenAI — Backend Software Engineer, GTM Innovation

Role page: https://openai.com/careers/backend-software-engineer-gtm-innovation-san-francisco/

Signals relevant to the portfolio:

- durable workflow orchestration and long-running agent loops;
- context, memory, tools, and permissions;
- rigorous evaluation and feedback loops;
- production observability and measurable agent quality.

## Portfolio implication

The strongest near-term proof-of-work is not another chat interface. It is a compact systems portfolio that demonstrates:

1. failure reproduction and recovery;
2. durable, inspectable state transitions;
3. idempotency and explicit approval boundaries;
4. source-grounded outputs and evidence lineage;
5. routing decisions with measurable quality / latency / work tradeoffs;
6. observability and evaluation artifacts;
7. clear limits on what the implementation proves.

## Hearth Orchestrator milestone sequence

### Milestone A — Commit Reliability Lab

Status: source and local evidence exist.

Deliverable target:

- counterexample showing check/write race;
- serialized local commit gateway;
- replay and stale-state handling;
- crash/interruption tests;
- public explanation of assumptions and non-goals.

### Milestone B — Source-Grounded Change Review

Deliverable target:

- frozen public/synthetic corpus;
- version/digest-preserving citations;
- supported/disputed/unresolved findings;
- contradiction fixtures and prompt-injection fixtures;
- evaluation rubric with human-adjudicated examples.

### Milestone C — Evidence-Backed Router

Deliverable target:

- deterministic rule route;
- retrieval route;
- model/tool route;
- clarification route;
- human-review route;
- bounded work/tool-call caps;
- decision trace and reason codes;
- fixed-workflow baseline comparison.

The router should earn its complexity through measured results; it should not be assumed superior because it is more agentic.

## Suggested interview framing

The project demonstrates how to move from a plausible AI workflow to a more dependable agent system by exposing failure modes, enforcing explicit boundaries, and measuring whether additional orchestration actually improves outcomes.
