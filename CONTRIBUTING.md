# Contributing to Utocoin Improvement Proposals

## Before opening a proposal

Discuss substantial proposals publicly before requesting a UIP number. A proposal should have a clear motivation, a sufficiently complete specification, and an identified author who will maintain it.

Authors must not assign their own number. New proposals should initially use a descriptive filename such as `uip-tapscript-example.md` and set `UIP: ?` and `Assigned: ?` in the preamble. A UIP editor assigns the number when the proposal is accepted into the repository.

UIP-1, UIP-2, and UIP-3 are bootstrap documents assigned when this repository was created.

## Language and format

- Normative documents must be written in English.
- Use Markdown and the RFC 822-style preamble shown in `uip-template.md`.
- Use the terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in their RFC 2119 sense.
- Separate normative requirements from examples and rationale.
- Specify byte order, serialization, length limits, failure behavior, and extensibility rules wherever relevant.
- Link external specifications using stable URLs and identify the referenced revision or commit.
- Published references must be publicly accessible. Do not cite private repositories, internal pull requests, or internal commit identifiers; use repository-local specifications and vectors until a public implementation is available.

## Required sections

A Specification UIP must include:

- Abstract
- Motivation
- Specification
- Rationale
- Backward Compatibility
- Security Considerations
- Reference Implementation, when applicable
- Test Vectors, when applicable
- Copyright

Process and Informational UIPs may omit sections that do not apply, but must still include a preamble, Abstract, Motivation, and Copyright.

## Auxiliary files

Auxiliary files for `uip-NNNN.md` belong in `uip-NNNN/`. This includes reference implementations, diagrams, generated scripts, and machine-readable test vectors. A top-level shared `examples/` directory is intentionally not used.

Test vectors that exercise consensus or interoperability requirements must be deterministic and independently reproducible. When a proposal defines a hash, at least one known-answer vector must contain the complete preimage serialization and expected digest.

## Status and versions

The statuses are:

- **Draft**: under active design and review.
- **Complete**: the specification is considered stable and recommended for adoption.
- **Deployed**: the specification is in active use or its consensus deployment has activated.
- **Closed**: no longer pursued or no longer in use.

Draft versions use `0.x.y`. Promotion to Complete uses `1.0.0`. Breaking specification changes increment the major version, compatible additions increment the minor version, and clarifications or test-vector fixes increment the patch version.

## Pull requests

A proposal pull request should explain:

- the problem being solved;
- the exact interoperability or consensus surface being standardized;
- alternatives considered;
- compatibility and deployment implications;
- how the test vectors were generated and verified.

Changes to consensus specifications should be reviewed independently from production-network activation parameters whenever practical.
