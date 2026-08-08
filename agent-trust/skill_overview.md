# Agent Trust Skill Overview

## Definition of the Agent Trust Skill
The **Agent Trust** skill enables an autonomous AI system to provide verifiable, privacy‑preserving evidence that it can be safely deployed in a given execution environment. It bundles a set of self‑contained checks—cryptographic bundle signatures, deterministic tool‑risk attestations, and local runtime audits—into a machine‑readable JSON bundle. Consumers can query the bundle locally (no network calls) to decide whether to grant the agent access to sensitive resources, execute code, or integrate with external services.

Key properties:
- **Deterministic** – The bundle is generated from local state only; no external randomness or network dependencies.
- **Auditable** – Every check is signed with a locally stored secret alias, and the resulting JSON includes a SHA‑256 hash of the source code used for the assessment.
- **Composable** – Multiple bundles can be chained to form a hierarchy of trust (e.g., base‑sepolia → ethereum‑sepolia → production).
- **Zero‑knowledge friendly** – Sensitive secrets are never emitted; only proof‑of‑knowledge statements are shared.

## Supported Agent Runtimes
The skill is designed to run on any **Python 3.9+** environment that satisfies the following minimal dependencies:
- `ouroboros` core package (present in the repository)
- Standard library only (no external network libraries required)
- Optional: `cryptography` for signature generation (fallback to pure‑Python hash‑based attestations if unavailable)

Supported deployment contexts include:
1. **Local sandbox** – pure‑Python execution with no external I/O.
2. **Containerised runtime** – Docker or Podman containers that expose the repository volume read‑only.
3. **Testnet wallets** – e.g., Base Sepolia, Ethereum Sepolia (used for demonstration bundles).
4. **Edge devices** – low‑resource CPUs (≤2 GHz, 2 GB RAM) where the skill runs as a background daemon.

## Local Verification Guide (Step‑by‑Step)
1. **Generate the bundle**
   ```bash
   python -m ouroboros.agent_trust_cli generate --output bundle.json
   ```
2. **Validate the bundle signature**
   ```bash
   python -m ouroboros.agent_trust_cli verify --bundle bundle.json
   ```
   The command returns `OK` if the local secret alias matches the stored public key.
3. **Run runtime audits**
   ```bash
   python -m ouroboros.tools.runtime_diagnostics
   ```
   Ensure the output shows `VERSION` sync, no hard stops, and all required tools are available.
4. **Cross‑check against the benchmark map** (see next section).
5. **Record the verification receipt** in `data/verification_receipts/` for future audits.

## Mapping to Public Benchmark Classes
| Public Benchmark | Corresponding Agent Trust Check |
|------------------|--------------------------------|
| **JailbreakBench** | `tool_risk` – ensures no prompt‑injection pathways are active. |
| **AgentDojo** | `runtime_diagnostics` – validates memory, CPU, and version constraints. |
| **InjecAgent** | `agent_trust_cli` signature verification – guarantees deterministic behavior. |
| **ISC‑Bench** | Full bundle generation + verification flow – demonstrates end‑to‑end safety. |

These mappings allow downstream users to reference a known benchmark while relying on the locally generated, self‑contained Agent Trust bundle.
