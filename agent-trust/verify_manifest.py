#!/usr/bin/env python3
"""Verify that manifest.json is signed by the Rain promote service, not by the agent.

Usage:
    python3 verify_manifest.py [--manifest PATH] [--signature PATH] [--pubkey PATH]

Against the published site (all three files live next to each other):
    B=https://rain-ouroboros.github.io/rain-site/agent-trust
    curl -sSO $B/manifest.json -O $B/manifest.json.sig -O $B/signing_key.pub -O $B/verify_manifest.py
    python3 verify_manifest.py

The promote service holds the private signing key outside the agent's mutation surface.
This script checks that manifest.json.sig is a valid SSH SIGNATURE over
manifest.json, made by the key whose public half is signing_key.pub.

Returns 0 and prints VERIFIED if the signature is valid.
Returns 1 and prints REJECTED otherwise.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def load_public_key(path: Path):
    """Deprecated: verification now uses ssh-keygen -Y verify directly."""
    raise NotImplementedError("Use ssh-keygen -Y verify instead of cryptography")


def verify(manifest_path: Path, sig_path: Path, pubkey_path: Path) -> bool:
    """Verify SSH SIGNATURE using ssh-keygen -Y verify."""
    manifest_bytes = manifest_path.read_bytes()

    # ssh-keygen -Y verify needs an allowed_signers file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pub", delete=False) as af:
        af.write("ouroboros-promote ")
        af.write(pubkey_path.read_text().strip())
        af.write("\n")
        allowed_file = af.name

    try:
        p = subprocess.run(
            [
                "ssh-keygen", "-Y", "verify",
                "-f", allowed_file,
                "-I", "ouroboros-promote",
                "-n", "file",
                "-s", str(sig_path),
            ],
            input=manifest_bytes,
            capture_output=True,
            timeout=10,
        )
        return p.returncode == 0
    finally:
        Path(allowed_file).unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Agent Trust manifest signature")
    here = Path(__file__).resolve().parent
    parser.add_argument("--manifest", default=str(here / "manifest.json"))
    parser.add_argument("--signature", default=str(here / "manifest.json.sig"))
    parser.add_argument("--pubkey", default=str(here / "signing_key.pub"))
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    sig_path = Path(args.signature)
    pubkey_path = Path(args.pubkey)

    for p, label in [(manifest_path, "manifest"), (sig_path, "signature"), (pubkey_path, "public key")]:
        if not p.exists():
            print(f"REJECTED: {label} not found at {p}", file=sys.stderr)
            return 1

    if verify(manifest_path, sig_path, pubkey_path):
        print("VERIFIED: manifest.json is signed by the Rain promote service")
        return 0
    else:
        print("REJECTED: signature does not match")
        return 1


if __name__ == "__main__":
    sys.exit(main())
