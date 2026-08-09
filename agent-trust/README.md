# Agent Trust Manifest

> **⚠️ Early-stage / alpha software.** Agent Trust is under active development. The manifest returns advisory receipts — the application owns enforcement. Not yet published on PyPI; install from GitHub source. See [Current Limitations](#current-limitations).

## What is this?

Agent Trust is a **local advisory receipt library** for AI-agent prompts, actions, scopes, and external tool descriptors. It returns deterministic allow/review/quarantine decisions for each checked item.

The public manifest in this site is a **sanitized static snapshot**. It does not contain a signature or raw public key, so third parties cannot cryptographically verify it and must not treat it as proof of current live state.

**What Agent Trust does:**
- Projects selected enforcement metadata into a sanitized manifest snapshot
- Returns advisory receipts: allow / review / quarantine per checked item

**What Agent Trust does NOT do:**
- Does not intercept LLM calls or execute tools
- Does not create a sandbox or runtime enforcement layer
- Does not replace application-level enforcement — the application owns enforcement

This architecture follows Pawel Twardziak's advice (LangChain Forum, July 2026): "The manifest should be generated from the enforced config — a projection of runtime-enforced boundaries, not a promise the agent makes."

## Where to find the manifest

The manifest interfaces are:

- **API endpoint:** `GET /api/agent-trust/manifest` (on the running Ouroboros server)
- **Static copy:** [`manifest.json`](manifest.json) (sanitized and potentially stale)
- **Landing page:** [`index.html`](index.html) — viewer for the static snapshot

## Verification status

The static artifact is inspectable JSON, not a cryptographic attestation. Real verification would require a canonical payload, an actual Ed25519 signature, and raw public-key bytes from an independently trusted channel. Those materials are not published on this site today.

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
  "signing": { "signature_available": false }
}
```

## Key architectural decisions

1. **Projection, not self-description.** Runtime code can generate a projection from enforcement objects. The public copy is sanitized and may lag that runtime.

2. **No public signature claim.** The current static snapshot deliberately reports that verification material is unavailable.

3. **Advisory receipts, application-owned enforcement.** The manifest returns allow/review/quarantine decisions, but the application — not Agent Trust — owns enforcement.

## Current Limitations

- **Advisory only.** Agent Trust returns receipts (allow/review/quarantine) — it does not enforce them. The application owns enforcement.
- **Alpha/early-stage.** The API and manifest format may change. Not yet production-hardened.
- **Not on PyPI.** Install from GitHub source: `pip install git+https://github.com/Rain-ouroboros/agent-trust.git`
- **Static snapshot is not verifiable.** No signature or raw public key is currently published on this site.
- **No LLM interception.** Agent Trust does not intercept LLM calls or execute tools — it operates on the configuration layer.
- **No sandbox.** Agent Trust is not a sandbox or container runtime.

## For third-party consumers

Treat the public snapshot as advisory metadata only. Check its age and declared mode, review the listed gates and boundaries, and require independently authenticated signature material before making a trust decision.

## Related

- **BIBLE.md** — Rain's Constitution (Principle 0: Agency, Principle 2: Self-Creation)
- **agent_trust_boundaries.py** — boundary catalog and enforcement logic
- **agent_trust_manifest.py** — manifest generation from live enforcement config
- **tools/verify_agent_trust_manifest.py** — verification tool
