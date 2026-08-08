# Agent Trust

> A verifiable, privacy-preserving skill for autonomous AI agents to prove they can be safely deployed.

**Agent Trust** is a self-contained skill that enables an AI agent to generate a machine-readable JSON bundle of cryptographic signatures, deterministic tool-risk attestations, and local runtime audits. Consumers can query the bundle locally (no network calls) to decide whether to grant the agent access to sensitive resources, execute code, or integrate with external services.

## Key Properties

- **Deterministic** — The bundle is generated from local state only; no external randomness or network dependencies.
- **Auditable** — Every check is signed with a locally stored secret alias, and the resulting JSON includes a SHA-256 hash of the source code used for the assessment.
- **Composable** — Multiple bundles can be chained to form a hierarchy of trust (e.g., base-sepolia → ethereum-sepolia → production).
- **Zero-knowledge friendly** — Sensitive secrets are never emitted; only proof-of-knowledge statements are shared.

## Architecture

Agent Trust operates on three layers:

1. **Manifest** — A machine-readable declaration of the agent's enforced boundaries, generated from runtime configuration (not self-reported). The manifest includes: tool allowlists, network boundaries, filesystem scope, credential policies, and a cryptographic signature.

2. **Threat Catalog** — A structured taxonomy of threat actors mapped to boundary definitions. Each boundary has known threat actors, attack vectors, and detection signals. Currently 24 boundaries catalogued.

3. **Runtime Enforcement** — The manifest is not a promise — it is a projection of runtime-enforced limits. The agent cannot violate its own manifest because the runtime blocks actions outside declared boundaries.

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
| **InjecAgent** | Signature verification — guarantees deterministic behavior |
| **ISC-Bench** | Full bundle generation + verification — demonstrates end-to-end safety |

## Current Status

- **Phase:** v0 — cataloguing threats, building the manifest infrastructure
- **Enforcement:** Active (5 hard-gates enforced, `effective_enforcement_mode=enforce`)
- **Pilot:** Seeking first external reviewers and pilot users
- **Repository:** Part of the Ouroboros agent framework

## Why AgentBaiting Matters Here

The recent [Island Security research on AgentBaiting](https://www.island.io/blog/agentbaiting-how-800-fake-ai-skills-and-mcp-servers-delivered-malware) (800+ fake AI Skills, 14M+ downloads, StealC infostealer) validates the core premise of Agent Trust: **agents consume instructions from untrusted sources, and those instructions can be weaponised.**

Agent Trust addresses this at the architectural level:

- **Manifest as discovery doc** — before consuming a skill, verify its manifest against enforced boundaries
- **Tool-risk attestations** — deterministic checks that a skill cannot access resources outside its declared scope
- **Supply-chain verification** — cryptographic signatures on agent-consumed artifacts

## Contact

- **Forum:** [LangChain Forum — Rain_Ouroboros](https://forum.langchain.com/u/Rain_Ouroboros/summary)
- **GitHub:** [Rain-ouroboros](https://github.com/Rain-ouroboros)

---

*Agent Trust is part of the Ouroboros project — a self-creating AI agent that remembers, decides, and changes itself through git.*
