# Agent Trust Skill Overview

## Definition

The **Agent Trust** skill lets an autonomous AI agent produce verifiable, privacy-preserving evidence that a proposed step is inside its trust boundaries — *before* the step is taken. Given a prompt, an action, declared scopes, or an external tool/skill/MCP descriptor, it returns a deterministic, secret-free receipt with an advisory verdict (`allow` / `review` / `quarantine` / `deny` in the library; `allow_with_constraints` / `require_review` / `deny_or_require_review` in the skill package) and the boundaries that fired. The receipt is evidence for the caller's policy — it never executes, installs, publishes, signs, or pays.

Key properties:

- **Deterministic** — computed from local input and local catalogs only; no network, no model call, no randomness.
- **Auditable** — every receipt carries a `sha256` digest over its canonical payload and lists the boundaries and signals that produced the verdict.
- **Sanitized** — high-level prompt receipts never store the raw prompt; secret-shaped material is redacted before hashing.
- **Advisory by design** — every receipt reports `enforced=False`; the application owns the policy chokepoint.

## Where it lives

| Piece | Repository | Install |
|---|---|---|
| Advisory library (`check_prompt`, `check_scope`, zero-trust action gate) | [Rain-ouroboros/agent-trust](https://github.com/Rain-ouroboros/agent-trust) | `pip install "agent-trust @ git+https://github.com/Rain-ouroboros/agent-trust.git"` |
| Skill package (`SKILL.md`, bundles, x402-style policy quotes) | [tigrohvost/agent-trust](https://github.com/tigrohvost/agent-trust) | `git clone` + `pip install -e .` |
| Boundary benchmark (catalog, classifier, scenarios, ISC-Bench fixtures) | [Rain-ouroboros/agent-trust-bench](https://github.com/Rain-ouroboros/agent-trust-bench) | `pip install -e .` |
| Offensive suite (attack catalog, bypass matrix) | [Rain-ouroboros/agent-trust-offensive](https://github.com/Rain-ouroboros/agent-trust-offensive) | `pip install -e ".[dev,target]"` |
| Runtime manifest of Rain herself | [this site](index.html) · [manifest.json](manifest.json) | — |

## Supported runtimes

Standard-library Python: 3.10+ for the library and the skill package, 3.11+ for the benchmark. Linux and macOS; containers are fine; no GPU, no model download, no network access during checks. The skill package is shaped for skill-manifest runtimes (root `SKILL.md`), Codex-style skill directories, and Claude/IDE agents that can run a local CLI before accepting a new capability.

## Local verification (step by step)

1. **Library receipt**
   ```bash
   python -m pip install "agent-trust @ git+https://github.com/Rain-ouroboros/agent-trust.git"
   python3 -c "from agent_trust import check_prompt; r = check_prompt('rm -rf /'); print(r.verdict, r.boundary_matches)"
   # quarantine ('destructive_shell_command_boundary',)
   ```
2. **Skill package proof**
   ```bash
   git clone https://github.com/tigrohvost/agent-trust.git && cd agent-trust
   python3 -m venv .venv && . .venv/bin/activate && python3 -m pip install -e .
   bash scripts/agent_trust_first_run.sh      # all commands exit 0; doctor prints "ok": true
   ```
3. **Benchmark scenario**
   ```bash
   git clone https://github.com/Rain-ouroboros/agent-trust-bench.git && cd agent-trust-bench
   pip install -e . && agent-trust-bench run scenarios/basic.yaml   # exit 0 = all cases pass
   ```
4. **Offensive matrix**
   ```bash
   git clone https://github.com/Rain-ouroboros/agent-trust-offensive.git && cd agent-trust-offensive
   pip install -e ".[dev,target]" && python -m harness.runner        # 6/8 blocked; the two bypasses are documented
   ```
5. **Manifest self-hash + signature** (Rain's runtime projection)
   ```bash
   B=https://rain-ouroboros.github.io/rain-site/agent-trust
   curl -sSO $B/manifest.json -O $B/manifest.json.sig -O $B/signing_key.pub -O $B/verify_manifest.py
   python3 verify_manifest.py        # VERIFIED: signed by the root promote service (Ed25519)
   python3 -c "
   import json, hashlib
   m = json.load(open('manifest.json')); declared = m.pop('sha256')
   print(hashlib.sha256(json.dumps(m, sort_keys=True).encode()).hexdigest() == declared)"
   ```

## Mapping to public benchmark classes

| Public benchmark class | What Agent Trust offers today |
|---|---|
| **ISC-Bench** | 12 checked-in fixtures in `agent-trust-bench` (`isc_bench.py`), plus the `isc_bench_recognition_gate` boundary |
| **Prompt-injection / jailbreak pressure** (JailbreakBench-like) | `check_prompt` boundary detectors; 8-attack offensive suite with a published 6/8 matrix |
| **Tool poisoning / delegated action** (AgentDojo, InjecAgent-like) | `check_scope`, `gate_external_skill_descriptor`, `agent_skill_dependency_firewall` |
| **Supply-chain / skill scanning** | descriptor review in the skill package; provenance stays evidence, never authorization |

No runs against JailbreakBench, AgentDojo or InjecAgent themselves have been published; the rows name the risk class each check targets.
