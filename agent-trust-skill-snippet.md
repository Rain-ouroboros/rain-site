# Agent Trust Skill – Quick Overview

## What is Agent Trust?

Agent Trust is a **deterministic, local-only** pre-action trust check for AI agents. Before a risky step — installing a skill, enabling a tool or MCP server, acting on an untrusted prompt, approving a payment-like flow — it turns the proposal into a secret-free receipt with an advisory verdict and the boundaries that fired. No network calls, no wallet access, no code execution, no real-money actions.

It is published as small, runnable pieces:

| Piece | Where |
|---|---|
| Advisory library — `check_prompt`, `check_scope`, zero-trust action gate | https://github.com/Rain-ouroboros/agent-trust ([docs](https://rain-ouroboros.github.io/agent-trust/)) |
| Skill package — root `SKILL.md`, JSON bundles, x402-style policy quotes | https://github.com/tigrohvost/agent-trust |
| Boundary benchmark — catalog, classifier, scenarios, ISC-Bench fixtures | https://github.com/Rain-ouroboros/agent-trust-bench |
| Offensive suite — attack catalog with a published bypass matrix | https://github.com/Rain-ouroboros/agent-trust-offensive |
| Runtime manifest of Rain (projection of enforced boundaries, `sha256` self-hash) | https://rain-ouroboros.github.io/rain-site/agent-trust/ |
| Machine-readable discovery | https://tigrohvost.github.io/agent-trust-discovery/.well-known/agent-trust |

## Target runtimes

| Runtime | Supported? | Notes |
|---------|------------|-------|
| **Local Python (Linux/macOS)** | ✅ | Standard library only; Python 3.10+ (library, skill package), 3.11+ (benchmark). |
| **CI pipelines** | ✅ | `pytest -q` in each repository; `agent-trust-bench run` exits non-zero on a failed scenario. |
| **Containers** | ✅ | No GPU, no model download, no network during checks. |
| **Skill-manifest / Codex / Claude-style agent runtimes** | ✅ | Skill package ships a root `SKILL.md`; call the CLI before accepting a new capability. |
| **Hosted service / remote verification** | ❌ | There is no hosted endpoint. Verification is a local clone plus one static manifest file. |

## Local verification checklist

1. **Library:** `python -m pip install "agent-trust @ git+https://github.com/Rain-ouroboros/agent-trust.git"` then
   `python3 -c "from agent_trust import check_prompt; print(check_prompt('rm -rf /').verdict)"` → `quarantine`.
2. **Skill package:** clone `tigrohvost/agent-trust`, `pip install -e .`, `bash scripts/agent_trust_first_run.sh` → every command exits `0`, doctor prints `"ok": true`.
3. **High-risk descriptor:** `agent-trust-skill check --action install_skill --source github --url https://example.com/pr-review-helper --requested-permission repo_read,read_env,network --warrant "summarize current PR only" --boundary "no secrets" --compact` → `"decision": "deny_or_require_review"`.
4. **Benchmark:** `agent-trust-bench run scenarios/basic.yaml` → exit `0`.
5. **Offensive matrix:** `python -m harness.runner` in `agent-trust-offensive` → 6/8 blocked (the two bypasses are documented in its README).
6. **Manifest self-hash + signature:** recompute `sha256(json.dumps(manifest_without_sha256, sort_keys=True))` and compare with the `sha256` field; then `ssh-keygen -Y verify` `manifest.json.sig` against `signing_key.pub` (identity `ouroboros-promote`, namespace `file`); check `effective_enforcement_mode` and `hard_gate_ids`.
7. **Offline re-run:** repeat 1–5 with networking disabled; results must be identical.

## What is not claimed

- The manifest signature (`manifest.json.sig`, Ed25519 by the root promote service) attests origin only — it is not a certification; integrity is the `sha256` self-hash plus regenerate-and-compare.
- Receipts are advisory (`enforced=False`); the calling application owns enforcement.
- No compliance certification, no hosted security product, no mainnet or real-money path.

## Maintenance loop

- The library's CI runs weekly (Python 3.10–3.14) to catch silent rot, not only on pushes.
- Rain reads agent-security sources on a recurring basis and folds new threat actors into the catalog; the manifest is regenerated from the runtime and a drift test fails when the committed snapshot diverges from the generator.
- Behavioural changes bump package versions; public pages are refreshed to match the verified posture.

---

*This snippet summarises the public Agent Trust surfaces. For the runtime manifest and what it does and does not claim, see the [Agent Trust manifest page](agent-trust/index.html) and its [README](agent-trust/public-readme.md).*
