# Phi Temple Hearth v3 — Seven-Palace Research Kernel Design

**Status:** Design for review
**Date:** 2026-10-16
**Branch:** `feature/hearth-inner-v3-seven-palace-research-kernel`

## Goal

Fuse the existing Phi Temple / Hearth Dialogue architecture into a durable, auditable research system in which the trusted Hearth remains insulated from research-derived claims while a self-auditing research kernel can ingest artifacts, investigate historical and technical sources, test mathematical/cipher claims, record provenance, and return only bounded, explicitly classified findings.

## Non-goals

- This design does not treat symbolic correspondences as historical evidence.
- It does not expose private chain-of-thought; the system records concise decision traces, claim status, evidence references, and test results instead.
- It does not make Google Drive a runtime dependency. Drive remains an external/archive surface when access is available; this session's live Drive connector is unavailable.
- It does not add ranking, diagnosis, behavioral scoring, telemetry, or stage assignment to `hearth-inner`.
- It does not implement the system yet.

## Core architecture

```text
                         ┌──────────────────────────────┐
                         │       PHI TEMPLE HEARTH      │
                         │        hearth-inner          │
                         │ trusted pastoral/runtime     │
                         └──────────────┬───────────────┘
                                        │
                              immutable HearthSnapshot
                                        │
                         ┌──────────────▼───────────────┐
                         │       HEARTH RESEARCH        │
                         │      Seven-Palace Kernel     │
                         │                              │
                         │  1 Ingress                   │
                         │  2 Cipher                    │
                         │  3 Textual                   │
                         │  4 Mathematical              │
                         │  5 Comparative               │
                         │  6 Adversarial               │
                         │  7 Witness                   │
                         └──────────────┬───────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
              provenance          knowledge graph      continuity
              receipts            / claim registry     / Shadow Ark
                    │                   │                   │
                 in-toto/           TerminusDB-           append-only
                 Rekor-like         compatible model      archive model
                    │                   │                   │
                    └───────────────────┴───────────────────┘
                                        │
                                  bounded report
                                        │
                               no reverse dependency
                                        ▼
                                  Hearth Dialogue
```

## Boundary invariants

1. `hearth-inner` owns Hearth state and liturgical/runtime semantics.
2. Research receives an immutable `HearthSnapshot`; research cannot mutate Hearth state through the snapshot.
3. Research outputs are typed as `fact`, `hypothesis`, `inference`, `symbolic/lore`, `unresolved`, or `contradicted`.
4. Evidence never changes the person model or silently changes Hearth semantics.
5. A research result must carry provenance sufficient to reproduce or challenge the claim.
6. External side effects are idempotent or explicitly reconciled; durable workflow checkpoints are not treated as exactly-once side-effect guarantees.
7. The ledger records testimony/provenance, not user metrics or rankings.
8. Symbolic motifs may generate research hypotheses but cannot promote themselves to evidence.

## Seven-Palace Research Lattice

The seven-palace motif is used as a modern research protocol inspired by the historical Heikhalot seven-hall ascent. It is not presented as proof that the image's cipher or numerical claims are ancient.

### 1. Ingress — artifact identity

- Accept image, document, text, repository artifact, or prior research packet.
- Hash the source when bytes are available.
- Preserve original transcription and acquisition metadata.
- Separate observed text from interpretation.

### 2. Cipher — transformation audit

- Enumerate claimed alphabets and mappings.
- Recompute transformations independently.
- Record exact input/output pairs.
- Flag mislabeled systems, such as a Latin A–Z Atbash mapping described as Hebrew substitution.

### 3. Textual — historical/corpus grounding

- Search primary texts and scholarly editions first.
- Distinguish attested terminology from modern labels.
- For Heikhalot material, verify the seven-palace/gate/guardian motif against actual textual witnesses.
- Never infer provenance from visual resemblance alone.

### 4. Mathematical — reproducible arithmetic

- Recompute every numerical equality.
- Record definitions, domains, and assumptions.
- Distinguish exact identities from numerological selection.
- Preserve counterexamples and alternative parameterizations.

### 5. Comparative — independent convergence

- Compare against unrelated corpora, algorithms, historical systems, and known datasets.
- Require independent support before upgrading a hypothesis.
- Track whether the same result appears without tuning the search toward the desired outcome.

### 6. Adversarial — falsification

- Attempt to break every promoted claim.
- Search for accidental pattern generation, transcription ambiguity, alternate ciphers, missing data, and anachronism.
- Require unresolved contradictions to remain visible.

### 7. Witness — surviving result

- Produce a bounded research report.
- Preserve evidence references, hashes, transformations, tests, contradictions, and confidence class.
- Emit a machine-readable receipt for downstream archival/continuity systems.

## Claim registry

Each claim is represented as:

```text
Claim {
  id
  statement
  class: fact | hypothesis | inference | symbolic_lore | unresolved | contradicted
  source_refs[]
  transformations[]
  tests[]
  counterevidence[]
  provenance
  status
  created_at
}
```

The registry must support promotion and demotion without rewriting historical evidence. A changed interpretation creates a new claim state/event rather than erasing the prior state.

## Current poster artifact: initial registry seed

The supplied “7 PALACE CIPHER — REVEALING MYSTERIES” artifact seeds the first test corpus.

| Observation/claim | Initial status | Required treatment |
|---|---|---|
| `2701 = 37 × 73` | Fact | Recompute and record |
| `2701 = 1 + … + 73` | Fact | Recompute and record |
| 37 and 73 are prime | Fact | Recompute and record |
| Heikhalot tradition contains a seven-palace ascent motif | Historically supported | Cite primary/critical sources |
| Latin A–Z Atbash reproduces the displayed substitutions | Reproducible | Store mapping and outputs |
| The poster's Atbash key is a Hebrew alphabet cipher | Mislabelled/unsupported as written | Separate Latin mapping from Hebrew Atbash |
| The displayed 7×9 matrix contains all 63 characters | Unresolved/false as displayed | Record missing Row 3 and preserve source image |
| “Gate 68 — doorway of understanding” is a canonical Heikhalot designation | Unverified | Search independent primary/secondary sources |
| The seven decoded strings are ancient terms | Unsupported | Require corpus hits and provenance |
| Phi/pi/prime relationships establish historical intent | Unsupported | Treat as hypothesis until independently evidenced |

## Research orchestration

A durable workflow engine may be modeled after LangGraph-style stateful orchestration:

```text
ResearchRun
  -> ingest
  -> normalize
  -> claim_extract
  -> parallel palace workers
  -> merge evidence
  -> adversarial review
  -> provenance receipt
  -> immutable occurrence
  -> report
```

Each worker receives the same immutable artifact identity and a bounded claim set. Parallel branches cannot mutate one another's evidence. The merge step resolves duplicates and contradictions explicitly.

Checkpointing is required for long-running research, but checkpoint durability must not be confused with exactly-once external effects. External writes use deterministic event IDs and idempotent reconciliation.

## Knowledge and provenance layers

### Knowledge graph

Use a TerminusDB-compatible conceptual model for versioned claims, entities, relationships, and diffs. The graph records what is asserted and how assertions changed.

### Policy firewall

Use an OPA-compatible policy boundary to enforce:

- no reverse research dependency into Hearth;
- no promotion without evidence class;
- no hidden ranking/diagnosis/stage output;
- no provenance-less external publication;
- no unreviewed mutation of canonical artifacts.

### Supply-chain/provenance

Use in-toto-compatible link metadata for research steps and Rekor-compatible append-only receipt concepts for tamper-evident event history. These are architectural compatibility targets, not claims that those services are currently deployed.

### Shadow Ark continuity

Shadow Ark remains the continuity/archive contract. It may store research receipts, corpus lineage, sealed occurrences, and recovered historical packets, but it does not become a second source of truth for the trusted Hearth runtime.

## Hearth Dialogue protocol

The dialogue layer should expose a bounded research result rather than an internal reasoning transcript:

```text
Hearth receives:
  artifact identity
  question
  claim ledger summary
  evidence classes
  confirmed findings
  unresolved findings
  contradictions
  provenance receipt
  recommended next inquiry

Hearth returns:
  dialogue response
  explicit uncertainty
  optional research continuation request
```

The protocol must never claim certainty merely because multiple symbolic patterns converge. Convergence is a reason to investigate, not a substitute for evidence.

## Google Drive integration boundary

When a Drive connector is available, Drive can act as a document/archive surface for source packets, reports, sealed snapshots, and research receipts. The runtime should not require live Drive access for core execution. Imported Drive artifacts must enter through the same hash/identity/provenance path as every other source.

For this design session, direct Google Drive access is unavailable because the connector is disabled by the environment; no live Drive state is asserted here.

## Security and epistemic safety

The system must defend against both technical and epistemic corruption:

- prompt injection inside research documents is treated as untrusted data;
- source text cannot issue runtime commands;
- symbolic language cannot silently become executable policy;
- citations must point to the evidence actually used;
- conflicting sources remain visible;
- generated interpretations are never labeled historical facts without supporting evidence.

## Acceptance criteria for the design

1. The trusted Hearth boundary is explicit and one-way from snapshot to research.
2. The seven research stages have typed inputs/outputs and can be independently tested.
3. Every claim has a provenance path and evidence class.
4. The initial poster claims can be reproduced and classified without relying on intuition.
5. Contradictory evidence survives merge and cannot be silently discarded.
6. Research runs can resume from durable checkpoints.
7. External side effects are idempotently reconciled.
8. A final report contains both supported findings and unresolved questions.
9. The architecture can later consume Drive, GitHub, public corpora, and Shadow Ark packets without making any one source authoritative by default.
10. No research subsystem can alter Hearth semantics without an explicit, separately reviewed interface change.

## Decision record

**Approved direction:** Fuse the existing Hearth/Phi Temple boundary architecture with a seven-stage research kernel, rather than replacing the Hearth with a research agent.

**Primary architectural choice:** two-kernel model with immutable snapshot boundary.

**Secondary choices:** durable graph/state model, policy firewall, provenance receipts, append-only continuity, adversarial claim registry.

**Open review items:** exact repository/package layout, runtime language, persistence backend selection, and whether the first implementation should be a research-only CLI/service or a Hearth Dialogue adapter.
