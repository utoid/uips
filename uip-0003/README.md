# UIP-3 auxiliary files

`reference.py` is the canonical template generator for UIP-3 version 1. It constructs Payment, Expiry, and Slash script bytes; computes `OP_OUTPUTHASH`, TapLeaf, and TapBranch hashes; and emits the machine-readable vectors.

Run:

```text
python reference.py --self-test
python reference.py --dump
```

`template-test-vectors.json` is the checked-in output of `python reference.py --dump`. The transaction signatures named in witness layouts are transaction-specific and are not included as fixed byte strings. The two claim signatures are fixed BIP 340 known-answer values. The generator preserves these signature bytes but does not perform signature verification.

The reference code is for specification and testing. It is not hardened wallet software and does not implement signing, Taproot output-key elliptic-curve arithmetic, chain lookup, policy evaluation, or transaction construction.
