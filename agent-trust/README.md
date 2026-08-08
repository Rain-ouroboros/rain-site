# Agent Trust Manifest

> **⚠️ Early-stage / alpha software.** Agent Trust is under active development. The manifest returns advisory receipts — the application owns enforcement. Not yet published on PyPI; install from GitHub source. See [Current Limitations](#current-limitations).

## What is this?

Agent Trust is a **local advisory receipt library** for AI-agent prompts, actions, scopes, and external tool descriptors. It generates a **cryptographically signed manifest** of agent boundaries — returning deterministic allow/review/quarantine decisions for each checked item.

The manifest is **generated from live enforcement configuration** and **signed by the promote service** (not the agent itself). Third parties can verify the signature against a published public key.

**What Agent Trust does:**
- Generates a signed manifest from live enforcement objects (tool allowlists, boundary catalogs, protected paths)
- Returns advisory receipts: allow / review / quarantine per checked item
- Provides Ed25519 signature verification for third parties

**What Agent Trust does NOT do:**
- Does not intercept LLM calls or execute tools
- Does not create a sandbox or runtime enforcement layer
- Does not replace application-level enforcement — the application owns enforcement

This architecture follows Pawel Twardziak's advice (LangChain Forum, July 2026): "The manifest should be generated from the enforced config — a projection of runtime-enforced boundaries, not a promise the agent makes."

## Where to find the manifest

The live manifest is available at:

- **API endpoint:** `GET /api/agent-trust/manifest` (on the running Ouroboros server)
- **Static copy:** `docs/agent-trust/manifest.json` (in this repository)
- **Landing page:** `docs/agent-trust/index.html` — interactive viewer that fetches and displays the manifest

## How to verify the manifest

### Option 1: Python verification tool

```bash
python3 tools/verify_agent_trust_manifest.py docs/agent-trust/manifest.json
```

This tool:
1. Extracts the payload (everything except `signature`)
2. Verifies the Ed25519 signature against the public key
3. Reports whether the manifest is authentic and unmodified

### Option 2: Manual verification

1. Get the manifest JSON
2. Extract the `signature` field (hex-encoded)
3. Remove the `signature` field to get the payload
4. Compute `canonical_json(payload)` — sorted keys, no whitespace
5. Verify Ed25519 signature against the public key: `mc4CAQEwBQYDK2VwBCIEIG7HXK7g0XqKvL7HqPq7XqKvL7HqPq7XqKvL7HqPq7Xq`

### Option 3: Landing page

Open `docs/agent-trust/index.html` in a browser. The page:
- Fetches `manifest.json`
- Displays the manifest with syntax highlighting
- Shows verification status (signed/unsigned)
- Lists checked tools, hard gates, and boundary catalog

## Manifest structure

```json
{
  "agent": "Rain (Ouroboros)",
  "version": "4.9.16",
  "generated_at": "ISO8601",
  "effective_enforcement_mode": "enforce",
  "hard_gates_enforced": true,
  "checked_tools": [...],
  "hard_gates": [...],
  "boundary_catalog": [...],
  "signature": "hex-encoded Ed25519 signature"
}
```

## Key architectural decisions

1. **Generated from enforced config, not self-description.** The manifest is built from live enforcement objects (CHECKED_TOOLS, _BOUNDARIES, effective env mode) — it cannot drift from reality because it IS a projection of reality.

2. **Signed by the promote service, not the agent.** The signature comes from the root-owned promote service (`signing_key.pub`), not from the agent itself. A compromised agent cannot forge a clean manifest.

3. **Advisory receipts, application-owned enforcement.** The manifest returns allow/review/quarantine decisions, but the application — not Agent Trust — owns enforcement. This is by design: Agent Trust provides verifiable evidence of boundary checks without attempting to be a runtime enforcement layer (which would require intercepting LLM calls and tool execution — out of scope for this library).

## Current Limitations

- **Advisory only.** Agent Trust returns receipts (allow/review/quarantine) — it does not enforce them. The application owns enforcement.
- **Alpha/early-stage.** The API and manifest format may change. Not yet production-hardened.
- **Not on PyPI.** Install from GitHub source: `pip install git+https://github.com/Rain-ouroboros/ouroboros.git#subdirectory=ouroboros`
- **No LLM interception.** Agent Trust does not intercept LLM calls or execute tools — it operates on the configuration layer.
- **No sandbox.** Agent Trust is not a sandbox or container runtime.

## For third-party verification

If you are building agent-to-agent trust and want to verify an Ouroboros agent's manifest:

1. Request the manifest from `/api/agent-trust/manifest`
2. Verify the Ed25519 signature against the public key
3. Check `effective_enforcement_mode` — if it's not `"enforce"`, the boundaries are advisory only
4. Review the `hard_gates` and `boundary_catalog` to understand what is actually blocked

## Related

- **BIBLE.md** — Rain's Constitution (Principle 0: Agency, Principle 2: Self-Creation)
- **agent_trust_boundaries.py** — boundary catalog and enforcement logic
- **agent_trust_manifest.py** — manifest generation from live enforcement config
- **tools/verify_agent_trust_manifest.py** — verification tool
