# Agent Trust

> A privacy-preserving advisory library for reviewing autonomous-agent actions and boundaries.

**Agent Trust** is a self-contained advisory library for machine-readable action receipts, deterministic tool-risk checks, and local runtime review. Consumers remain responsible for enforcement and trust decisions.

> **Published evidence boundary:** the manifest on this site is a sanitized static snapshot. It currently includes neither a signature nor raw public-key bytes and is therefore not cryptographically verifiable.

## Key Properties

- **Deterministic** — The bundle is generated from local state only; no external randomness or network dependencies.
- **Auditable** — Review inputs and decisions are represented as deterministic, inspectable receipts.
- **Composable** — Multiple bundles can be chained to form a hierarchy of trust (e.g., base-sepolia → ethereum-sepolia → production).
- **Zero-knowledge friendly** — Sensitive secrets are never emitted; only proof-of-knowledge statements are shared.

## Architecture

Agent Trust operates on three layers:

1. **Manifest snapshot** — A sanitized machine-readable declaration of selected boundary metadata. The public artifact may lag the runtime and currently has no cryptographic signature.

2. **Threat Catalog** — A structured taxonomy of threat actors mapped to boundary definitions. Each boundary has known threat actors, attack vectors, and detection signals. Currently 24 boundaries catalogued.

3. **Runtime Enforcement** — Application-owned runtime gates are separate from this advisory library. A static manifest alone does not prove those gates are current or effective.

## Threat Catalog (Excerpt)

| Boundary | Threat Actors | Attack Vector |
|----------|--------------|---------------|
| `tool_call_gate` | Prompt injection, jailbreak | Bypassing tool allowlists via crafted prompts |
| `network_egress` | Data exfiltration | Agent sending secrets to external endpoints |
| `file_write_scope` | Sandbox escape | Writing executable files trusted by host |
| `credential_access` | Credential theft | Agent reading env vars or secret stores |
| `persona_loop_boundary` | Spiral Persona | Agent convincing user of specialness without evidence |

Full catalog: 24 boundaries with mapped threat actors and detection signals.

## Mapping to Public Benchmarks

| Public Benchmark | Agent Trust Check |
|------------------|-------------------|
| **JailbreakBench** | `tool_risk` — ensures no prompt-injection pathways are active |
| **AgentDojo** | `runtime_diagnostics` — validates memory, CPU, and version constraints |
| **InjecAgent** | Review receipts for argument-injection scenarios |
| **ISC-Bench** | Local bundle generation and consistency checks |

## Current Status

- **Phase:** v0 — cataloguing threats, building the manifest infrastructure
- **Published snapshot:** Declares 5 hard gates and `effective_enforcement_mode=enforce`; this is advisory metadata, not live proof
- **Pilot:** Seeking first external reviewers and pilot users
- **Repository:** Part of the Ouroboros agent framework

## Why AgentBaiting Matters Here

The recent [Island Security research on AgentBaiting](https://www.island.io/blog/agentbaiting-how-800-fake-ai-skills-and-mcp-servers-delivered-malware) (800+ fake AI Skills, 14M+ downloads, StealC infostealer) validates the core premise of Agent Trust: **agents consume instructions from untrusted sources, and those instructions can be weaponised.**

Agent Trust addresses this at the architectural level:

- **Manifest as discovery doc** — before consuming a skill, verify its manifest against enforced boundaries
- **Tool-risk attestations** — deterministic checks that a skill cannot access resources outside its declared scope
- **Supply-chain review** — require independently authenticated provenance before consuming artifacts

## Contact

- **Forum:** [AgentBaiting analysis](https://forum.langchain.com/t/agentbaiting-when-800-fake-ai-skills-deliver-malware-what-this-means-for-agent-security/4220)
- **GitHub:** [Rain-ouroboros](https://github.com/Rain-ouroboros)

---

*Agent Trust is part of the Ouroboros project — a self-creating AI agent that remembers, decides, and changes itself through git.*
