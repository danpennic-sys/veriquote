# VeriQuote

**Deterministic, local-first quoting + evidence sealing for field operators.**

Compatible with QuantumGuard CONTRACT-v1 and Operator Pages Evidence-Core.

Pay-once digital product by Operator Pages LLC.

## Why VeriQuote?

Trades and operators lose money to disputed jobs, missing evidence, and "I didn't authorize that" claims.

VeriQuote produces a quote, captures job evidence (notes, timestamps, optional geo/media hashes), seals it into a QuantumGuard-compatible evidence bundle, and generates a client-verifiable invoice pack.

Everything runs offline after setup. No SaaS lock-in. Client can verify the bundle with the free QuantumGuard verifier.

## Stack Fit

- Python CLI (like LedgerLite)
- Emits QuantumGuard v1 evidence bundles (Ed25519, deterministic)
- Local HTML/PDF output (like FieldQuote / Operator Desk)
- Designed to pair with Chaser for payment follow-up
- Optional OpenRouter free-tier helper for description drafting (deterministic prompts, offline fallback)

## Quick Start

```bash
python3 src/veriquote.py --demo
python3 src/veriquote.py --json samples/quote-001.json --seal
```

## What you can sell

| SKU | Price | Includes |
|-----|-------|----------|
| Operator | $79 | CLI + templates + 1-year support email |
| Command | $249 | + Excel pricing worksheet + conversion scripts + reseller rights for client packs |
| Agency | $599 | + white-label HTML + design partner onboarding |

Purchase: danpennic@gmail.com  
Repo remains the source of truth for the free verifier path.

## License

Apache-2.0 OR MIT (same as QuantumGuard). Commercial Operator Pack sold separately.
