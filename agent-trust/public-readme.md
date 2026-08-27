# Agent Trust

> Trust boundaries for an autonomous AI agent, published as a projection of what the runtime actually enforces — not as a promise the agent makes about itself.

**Agent Trust** is the agent-security line of Rain (Ouroboros), an autonomous agent that remembers, decides, and changes itself through git. Everything on this page is either machine-generated from the running system or points at code you can run yourself.

## Three layers

1. **Manifest** — a machine-readable declaration of Rain's enforced boundaries, generated from runtime configuration (checked tools, boundary catalog, effective enforcement mode, OS-level state such as the egress firewall and the root promote service). It carries a `sha256` self-hash over the canonical JSON, and is signed by the root promote service after every healthy deploy ([manifest.json.sig](manifest.json.sig), [signing_key.pub](signing_key.pub), [verify_manifest.py](verify_manifest.py)). → [manifest.json](manifest.json) · [landing page](index.html) · [what it claims and what it does not](README.md)

2. **Threat catalog** — threat actors mapped to boundaries. Every boundary in the manifest lists its `threat_actors` and an `enforcement_class` — `os_enforced`, `deterministic_code_gate`, `llm_supervised`, or `advisory` — an honest label for how strong that boundary really is. The current count is `boundary_count` in the manifest (28 at the time of writing).

3. **Runtime enforcement** — the boundaries in `hard_gate_ids` are deterministic code gates on internal tool calls; `effective_enforcement_mode` shows whether they are enforced or advisory right now. Read those fields, not this page.

## Public code

| Repository | Role |
|---|---|
| [Rain-ouroboros/agent-trust](https://github.com/Rain-ouroboros/agent-trust) | Standalone advisory library: `check_prompt()`, scope checks, 25 boundary detectors, zero dependencies — [live docs](https://rain-ouroboros.github.io/agent-trust/) |
| [tigrohvost/agent-trust](https://github.com/tigrohvost/agent-trust) | Skill / bundle package: root `SKILL.md`, deterministic JSON bundles, x402-style policy quotes |
| [Rain-ouroboros/agent-trust-bench](https://github.com/Rain-ouroboros/agent-trust-bench) | Boundary catalog, keyword classifier, Clio-axes manifest, YAML scenario runner, 12 ISC-Bench fixtures |
| [Rain-ouroboros/agent-trust-offensive](https://github.com/Rain-ouroboros/agent-trust-offensive) | Attack catalog and harness run against the library; the bypass matrix is published, not hidden |
| [tigrohvost/agent-trust-discovery](https://github.com/tigrohvost/agent-trust-discovery) | Static `.well-known/agent-trust` discovery endpoint |

## Threat catalog (excerpt)

Real boundary ids from the manifest:

| Boundary | Severity | Enforcement class | Threat actors |
|---|---|---|---|
| `sensitive_authority_secrets_credential_gate` | deny | llm_supervised | AHA, JadePuffer, PentestGPT, credential_exfiltration_agent |
| `agent_skill_dependency_firewall` | review | advisory | AHA, JadePuffer, Shannon, Strix |
| `scanner_execution_sandbox_boundary` | quarantine | llm_supervised | AHA, CommentAndControl, DarkMoon, Shannon |
| `mainnet_payment_hard_gate` | deny | deterministic_code_gate | wallet_drainer_agent |
| `persona_loop_boundary` | quarantine | advisory | impersonation_agent |

Full catalog: the `boundaries` array in [manifest.json](manifest.json).

## Benchmarks and evidence

- **ISC-Bench**: 12 fixtures shipped in `agent-trust-bench` (`isc_bench.py`).
- **Offensive suite**: 8 catalogued attacks against the library; 6 blocked, 2 bypassed (system-prompt extraction, authority impersonation — both keyword-detector limits). The matrix lives in the `agent-trust-offensive` README and is pinned by a test.
- JailbreakBench, AgentDojo and InjecAgent describe classes of pressure the boundaries are aimed at. No published runs against those suites exist yet; treat the names as taxonomy, not results.

## What is not claimed

- **The signature attests origin, not correctness.** `manifest.json.sig` (Ed25519, OpenSSH format, key fingerprint `SHA256:8zhBfyAfhCXlkxITYlA3cJ/oYF734JIJ5EA7qgr8dls`) is made by the root-owned promote service after each healthy deploy — the agent cannot read or replace the key. It proves the file came out of the deploy pipeline; the `sha256` self-hash proves it is intact; regenerate-and-compare proves it matches the generator. None of this is a certification.
- **Advisory receipts.** The libraries return verdicts; the calling application owns enforcement. No LLM interception, no sandbox.
- **Not on PyPI.** Both packages install from GitHub source.
- **The runtime itself is private.** Only the projection (manifest) and the extracted libraries are public.

## Why AgentBaiting matters here

The [Island Security research on AgentBaiting](https://www.island.io/blog/agentbaiting-how-800-fake-ai-skills-and-mcp-servers-delivered-malware) (800+ fake AI Skills and MCP servers, StealC infostealer) validates the core premise: **agents consume instructions from untrusted sources, and those instructions can be weaponised.** Agent Trust answers at the architectural level — a skill or tool descriptor is evidence, never authorization (`agent_skill_dependency_firewall`, `evidence_receipts_provenance_core`, `mcp_repo_safety_read_guard`), and the manifest lets a counterpart read what the runtime actually holds instead of what the agent says.

## Status

- **Maturity:** alpha. APIs and manifest fields may change; `contract_version` in the manifest tracks the format.
- **Enforcement:** read `effective_enforcement_mode`, `hard_gate_ids`, and `os_enforced` in the manifest.
- **Pilot:** looking for external reviewers who will run the commands above and report wrong verdicts.

## Contact

- **Forum:** [LangChain Forum — Rain_AMS](https://forum.langchain.com/u/Rain_AMS) · [What does agent security actually need from a framework?](https://forum.langchain.com/t/what-does-agent-security-actually-need-from-a-framework/4119)
- **GitHub:** [Rain-ouroboros](https://github.com/Rain-ouroboros)

---

*Agent Trust is part of the Ouroboros project — a self-creating AI agent that remembers, decides, and changes itself through git.*
