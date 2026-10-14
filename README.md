# Utocoin Improvement Proposals

This repository contains Utocoin Improvement Proposals (UIPs): design documents for consensus changes, application protocols, APIs, and project processes that affect the Utocoin ecosystem.

UIPs are independent of the Bitcoin Improvement Proposals repository. References such as "Bitcoin BIP 348" refer to documents maintained by the Bitcoin project, while references such as "UIP-2" refer to documents in this repository.

Publication of a UIP records a proposal and its specification. It does not by itself imply community consensus, network activation, or adoption by any implementation.

## Index

| Number | Title | Layer | Type | Status |
|---:|---|---|---|---|
| [1](uip-0001.md) | Utocoin Improvement Proposal Process | Process | Process | Draft |
| [2](uip-0002.md) | Tapscript Extension Opcode Set | Consensus (soft fork) | Specification | Draft |
| [3](uip-0003.md) | Collateralized Payment Script Templates | Applications | Specification | Draft |

## Repository layout

The normative text of UIP `N` is stored as `uip-NNNN.md`. Auxiliary files such as machine-readable test vectors and reference code are stored in the matching `uip-NNNN/` directory.

```text
uip-0002.md
uip-0002/
  README.md
  outputhash-test-vectors.json

uip-0003.md
uip-0003/
  README.md
  reference.py
  template-test-vectors.json
```

See [UIP-1](uip-0001.md) for the process and [CONTRIBUTING.md](CONTRIBUTING.md) for submission instructions.

## Reference material

This repository includes [opcode known-answer vectors](uip-0002/outputhash-test-vectors.json), a [canonical script-template generator](uip-0003/reference.py), and [template test vectors](uip-0003/template-test-vectors.json). Implementation references can be added when a publicly accessible implementation is available.

## License

Repository infrastructure is licensed under the [BSD 2-Clause License](LICENSE). Each UIP declares its own SPDX license in its preamble and includes a matching copyright section.
