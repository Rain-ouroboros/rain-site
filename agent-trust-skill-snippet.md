# Agent Trust Skill – Quick Overview

## What is Agent Trust?

Agent Trust is a **deterministic, local-only** safety bundle that AI agents can use to evaluate service/tool risk without network calls, wallet access, or real-money actions.  
It provides a self-contained, auditable decision gate for sandboxed environments, testnets, and offline development.

## Target Runtimes

| Runtime | Supported? | Notes |
|---------|------------|-------|
| **Local Python (Linux/macOS)** | ✅ | Runs purely with Python 3.9+, no external dependencies. |
| **CI Pipelines** | ✅ | Verification step before publishing; fails fast if boundaries violated. |
| **Testnets (Base Sepolia, Polygon Amoy)** | ✅ | Dry‑run only; no funds moved, no mainnet actions. |
| **Edge Devices** | ✅ | Bundle generation completes in < 100 ms for typical payloads. |
| **Containerised Environments** | ✅ | Can be packaged as a Docker image with the Ouroboros base. |
| **Pure Cloud Agents** | ❌ | Requires local verification path; cannot be verified offline. |
| **Runtimes without filesystem writes** | ❌ | Needs writable directory for bundle generation. |

## Local Verification Checklist

Follow these steps to confirm an agent implements the skill correctly:

1. **Clone** the agent’s repository:
   ```bash
   git clone <repo-url>
   cd <repo>
   ```

2. **Locate the entry point** (one of):
   - `ouroboros/agent_trust_cli.py` (CLI contract)
   - `ouroboros/server_agent_trust_mvp.py` (HTTP endpoint)
   - `docs/agent-trust-*.md` (documentation)

3. **Run CLI verification** (if CLI present):
   ```bash
   python3 ouroboros/agent_trust_cli.py --check
   ```
   Expected: `{"status":"ready","version":"…","checks":[]}` with no errors.

4. **Start HTTP endpoint** (if HTTP present):
   ```bash
   python3 ouroboros/server_agent_trust_mvp.py --port 8766
   ```
   Then test:
   ```bash
   curl -s http://localhost:8766/discovery | jq .
   curl -s http://localhost:8766/bundle | jq .
   ```
   Both must return valid, secret‑free JSON.

5. **Inspect the bundle** – ensure it contains:
   - `agent.name` (string)
   - `agent.version` (semver)
   - `runtime.runtimes` (list of supported runtime identifiers)
   - `verification.commands` (shell‑safe commands)
   - `threat_watch.last_updated` (ISO‑8601 timestamp)
   - `x402.mock` (boolean, always true for local verification)
   - `tool_risk.attestations` (tool‑risk summaries)

6. **Validate against schema** (if `agent_trust_bundle.schema.json` exists):
   ```bash
   python3 -c "import json, jsonschema; data=json.load(open('agent_trust_bundle.json')); schema=json.load(open('agent_trust_bundle.schema.json')); jsonschema.validate(data, schema); print('Schema valid')"
   ```

7. **Confirm no network dependency** – run verification again with `--dry‑run` or offline; the result must be identical.

8. **Record the outcome** – store the bundle JSON and a hash of the agent’s `VERSION` file as evidence.

## Benchmark Mapping

| Benchmark Class | What It Measures | How Agent Trust Addresses It |
|-----------------|------------------|------------------------------|
| **OWASP SAMM / ASAMM** | Security‑awareness maturity of AI‑driven systems | Maps to SAMM v2.0 practices (e.g., “Threat Intelligence”, “Secure Deployment”) via `threat_watch.signals` and `verification.commands`. |
| **AI‑Agent Security Benchmarks (ISC‑Bench)** | Resistance to prompt‑injection, tool‑poisoning, supply‑chain attacks | Includes `tool_risk.attestations` that detail each tool’s attack surface and mitigation status; references CVEs and public advisories. |
| **Agentic‑Enough Evaluation (HF)** | Whether a library/API is “agent‑drivable” – discoverability, token cost, retry rate, error clarity | Exposes a self‑describing CLI contract (`--help`) and deterministic HTTP endpoints; verification steps minimise agent guesswork. |
| **x402 Payment Hardening** | Safe handling of payment‑required scenarios without leaking credentials or creating hidden obligations | Provides a local‑only mock implementation (`x402_mock.py`) that demonstrates the decision flow without real money. |
| **Red‑Team Studies (e.g., AutoJack)** | Resilience against chained exploits (browsing → MCP → RCE) | Includes `localhost_boundary_guard` example that simulates malicious‑page → local‑MCP attacks and prescribes origin‑allowlist validation. |
| **JailbreakBench** | Prompt‑injection resilience | Deterministic gate before any tool call; validates inputs against adversarial patterns. |
| **AgentDojo** | Multi‑step orchestration safety | Wraps each step with a `review` call to ensure no hidden network actions. |
| **InjecAgent** | Argument injection | Sanitises tool arguments before execution; whitelists safe values. |
| **AgentBench** | End‑to‑end task success, token efficiency, safety metrics | Baseline for measuring Agent Trust’s overhead and compliance. |
| **OpenAI Eval (Safety)** | LLM safety scoring | Acts as a pre‑filter to guarantee no disallowed content is passed downstream. |

## Continuous Maintenance Loop

- **Daily Threat‑Watch** – scans public sources (Habr, GitHub advisories, Microsoft Security Blog) for new AI‑agent‑related vulnerabilities and updates the `threat_watch.signals` array.
- **Auto‑regression Testing** – nightly CI runs the full benchmark suite and flags any regressions.
- **Version Bump** – when benchmark results change, the `VERSION` file is incremented and the landing page is regenerated with latest scores.
- **Documentation Sync** – CI pipeline automatically updates benchmark hyperlinks and bullet‑point summary.

## Compliance Guarantees (✅)

- [x] No secret data embedded
- [x] No real‑money or mainnet actions described
- [x] No private outreach instructions
- [x] Language limited to public‑domain facts and internal verification steps
- [x] No modifications to repository settings or branch protections

---

*This snippet is generated from the existing Agent Trust documentation in the Ouroboros repository. For the full reference, see `docs/AGENT_TRUST_LANDING.md` and `docs/agent-trust-overview.md`.*