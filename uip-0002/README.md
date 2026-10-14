# UIP-2 auxiliary files

`outputhash-test-vectors.json` contains independent known-answer vectors for the Utocoin-specific `OP_OUTPUTHASH` operation. Hashes are written in SHA-256 output byte order, which is also the byte order pushed onto the Script stack.

The vector format records the amount, scriptPubKey, complete serialized `CTxOut`, tag, and expected digest. `script_cases` additionally records valid and invalid zero-based indexes for a two-output transaction.

The Bitcoin-derived operations follow the pinned upstream specifications:

- Bitcoin BIP 347 for `OP_CAT`;
- Bitcoin BIP 348 for `OP_CHECKSIGFROMSTACK`;
- Bitcoin BIP 446 for `OP_TEMPLATEHASH`.

Repository-local application templates and vectors are provided in [UIP-3](../uip-0003.md) and its auxiliary directory.
