#!/usr/bin/env python3
"""VeriQuote — local-first quoting + QuantumGuard-compatible evidence sealing.
Operator Pages LLC. Deterministic. Offline after key setup.
"""
import argparse
import base64
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Minimal Ed25519 signing via PyNaCl if available, else deterministic stub for demo
try:
    from nacl.signing import SigningKey
    HAS_NACL = True
except ImportError:
    HAS_NACL = False

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def make_evidence_bundle(payload: dict, signing_key_hex: str | None = None) -> dict:
    payload_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload_hash = sha256_hex(payload_bytes)
    bundle = {
        "version": "1",
        "payload": base64.b64encode(payload_bytes).decode(),
        "payload_hash": payload_hash,
        "alg": "ed25519",
    }
    if HAS_NACL and signing_key_hex:
        sk = SigningKey(bytes.fromhex(signing_key_hex))
        sig = sk.sign(bytes.fromhex(payload_hash)).signature
        bundle["signature"] = sig.hex()
        bundle["public_key"] = sk.verify_key.encode().hex()
    else:
        # Demo stub — replace with real key for production
        bundle["signature"] = "0" * 128
        bundle["public_key"] = "0" * 64
        bundle["note"] = "DEMO STUB — install pynacl and provide --key for real Ed25519"
    return bundle

def load_or_create_sample() -> dict:
    return {
        "quote_id": "VQ-2026-001",
        "operator": "Operator Pages Field Demo",
        "client": "Acme Roofing Co.",
        "scope": "Roof inspection + gutter clean + photo evidence pack",
        "line_items": [
            {"desc": "Roof inspection (drone + ground)", "qty": 1, "unit": 185.00},
            {"desc": "Gutter clean (linear ft)", "qty": 120, "unit": 2.50},
            {"desc": "Evidence pack sealing", "qty": 1, "unit": 0.00},
        ],
        "notes": "All work performed under local ordinance. Photos hashed and attached as media refs.",
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "geo_hash": "optional-sha256-of-latlon",
        "media_hashes": ["optional-photo-hash-1", "optional-photo-hash-2"],
    }

def compute_totals(quote: dict) -> dict:
    sub = sum(i["qty"] * i["unit"] for i in quote["line_items"])
    tax = round(sub * 0.0, 2)  # operator sets tax externally
    return {"subtotal": sub, "tax": tax, "total": sub + tax}

def main():
    parser = argparse.ArgumentParser(description="VeriQuote — seal quotes as QuantumGuard evidence")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample quote")
    parser.add_argument("--json", type=str, help="Path to quote JSON")
    parser.add_argument("--seal", action="store_true", help="Emit QuantumGuard v1 bundle")
    parser.add_argument("--key", type=str, help="Hex Ed25519 private key (32 bytes)")
    parser.add_argument("--out", type=str, default="quote-bundle.json")
    args = parser.parse_args()

    if args.demo or not args.json:
        quote = load_or_create_sample()
    else:
        with open(args.json) as f:
            quote = json.load(f)

    totals = compute_totals(quote)
    quote["totals"] = totals
    print("=== VeriQuote Preview ===")
    print(json.dumps(quote, indent=2))
    print(f"\nTotal: ${totals['total']:.2f}")

    if args.seal or args.demo:
        bundle = make_evidence_bundle(quote, args.key)
        out_path = Path(args.out)
        out_path.write_text(json.dumps(bundle, indent=2))
        print(f"\nSealed bundle written to {out_path}")
        print("Verify with: qg verify quote-bundle.json   (from QuantumGuard)")
        if not HAS_NACL:
            print("Note: Install 'pip install pynacl' for real signatures.")

if __name__ == "__main__":
    main()
