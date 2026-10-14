#!/usr/bin/env python3
"""Reference script-template construction for UIP-3.

This implementation is intentionally small and is not a wallet. It constructs
the canonical script bytes and hashes used by the UIP-3 test vectors.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path
from typing import Any


OP_0 = 0x00
OP_1NEGATE = 0x4F
OP_1 = 0x51
OP_2 = 0x52
OP_3 = 0x53
OP_6 = 0x56
OP_VERIFY = 0x69
OP_TOALTSTACK = 0x6B
OP_FROMALTSTACK = 0x6C
OP_2DUP = 0x6E
OP_2SWAP = 0x72
OP_DROP = 0x75
OP_DUP = 0x76
OP_PICK = 0x79
OP_ROLL = 0x7A
OP_SWAP = 0x7C
OP_CAT = 0x7E
OP_SIZE = 0x82
OP_EQUAL = 0x87
OP_EQUALVERIFY = 0x88
OP_NOT = 0x91
OP_CHECKSIG = 0xAC
OP_CHECKSIGVERIFY = 0xAD
OP_CHECKLOCKTIMEVERIFY = 0xB1
OP_CHECKSIGFROMSTACK = 0xCC
OP_OUTPUTHASH = 0xCF

TAPSCRIPT_LEAF_VERSION = 0xC0
NUMS_INTERNAL_KEY = bytes.fromhex(
    "50929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0"
)


def tagged_hash(tag: str, payload: bytes) -> bytes:
    tag_hash = hashlib.sha256(tag.encode("utf-8")).digest()
    return hashlib.sha256(tag_hash + tag_hash + payload).digest()


def compact_size(value: int) -> bytes:
    if value < 0:
        raise ValueError("CompactSize cannot encode a negative value")
    if value < 253:
        return bytes([value])
    if value <= 0xFFFF:
        return b"\xfd" + struct.pack("<H", value)
    if value <= 0xFFFFFFFF:
        return b"\xfe" + struct.pack("<I", value)
    if value <= 0xFFFFFFFFFFFFFFFF:
        return b"\xff" + struct.pack("<Q", value)
    raise ValueError("CompactSize value is too large")


def encode_script_num(value: int) -> bytes:
    if value == 0:
        return b""
    negative = value < 0
    absolute = -value if negative else value
    encoded = bytearray()
    while absolute:
        encoded.append(absolute & 0xFF)
        absolute >>= 8
    if encoded[-1] & 0x80:
        encoded.append(0x80 if negative else 0)
    elif negative:
        encoded[-1] |= 0x80
    return bytes(encoded)


def push_data(value: bytes) -> bytes:
    if len(value) == 0:
        return bytes([OP_0])
    if len(value) <= 75:
        return bytes([len(value)]) + value
    if len(value) <= 255:
        return b"\x4c" + bytes([len(value)]) + value
    raise ValueError("reference templates do not push values larger than 255 bytes")


def push_int(value: int) -> bytes:
    if value == -1:
        return bytes([OP_1NEGATE])
    if value == 0:
        return bytes([OP_0])
    if 1 <= value <= 16:
        return bytes([OP_1 + value - 1])
    return push_data(encode_script_num(value))


def require_length(name: str, value: bytes, expected: int) -> None:
    if len(value) != expected:
        raise ValueError(f"{name} must be {expected} bytes")


def payment_script(alice_pubkey: bytes, pid: bytes) -> bytes:
    require_length("alice_pubkey", alice_pubkey, 32)
    require_length("pid", pid, 32)
    return b"".join(
        [
            bytes([OP_DUP, OP_SIZE]),
            push_int(32),
            bytes([OP_EQUALVERIFY, OP_TOALTSTACK, OP_SWAP, OP_SIZE]),
            push_int(32),
            bytes([OP_EQUALVERIFY, OP_SWAP, OP_SWAP]),
            push_data(pid),
            bytes([OP_CAT, OP_SWAP, OP_CAT]),
            push_data(alice_pubkey),
            bytes([OP_CHECKSIGFROMSTACK, OP_VERIFY]),
            push_data(alice_pubkey),
            bytes([OP_CHECKSIGVERIFY, OP_FROMALTSTACK, OP_CHECKSIG]),
        ]
    )


def expiry_script(alice_pubkey: bytes, expiry: int) -> bytes:
    require_length("alice_pubkey", alice_pubkey, 32)
    if expiry < 0 or expiry > 0x7FFFFFFF:
        raise ValueError("expiry must fit the non-negative ScriptNum range used by CLTV")
    return b"".join(
        [
            push_int(expiry),
            bytes([OP_CHECKLOCKTIMEVERIFY, OP_DROP]),
            push_data(alice_pubkey),
            bytes([OP_CHECKSIG]),
        ]
    )


def slash_script(
    alice_pubkey: bytes,
    stake_sid: bytes,
    burn_output_hash: bytes,
) -> bytes:
    require_length("alice_pubkey", alice_pubkey, 32)
    require_length("stake_sid", stake_sid, 32)
    require_length("burn_output_hash", burn_output_hash, 32)
    return b"".join(
        [
            push_data(alice_pubkey),
            bytes([OP_TOALTSTACK, OP_SIZE]),
            push_int(32),
            bytes([OP_EQUALVERIFY, OP_SWAP]),
            push_data(stake_sid),
            push_int(6),
            bytes([OP_PICK, OP_CAT]),
            push_int(2),
            bytes(
                [
                    OP_PICK,
                    OP_CAT,
                    OP_FROMALTSTACK,
                    OP_DUP,
                    OP_TOALTSTACK,
                    OP_CHECKSIGFROMSTACK,
                    OP_VERIFY,
                    OP_TOALTSTACK,
                    OP_SIZE,
                ]
            ),
            push_int(32),
            bytes([OP_EQUALVERIFY, OP_DUP, OP_TOALTSTACK, OP_SWAP, OP_SIZE]),
            push_int(32),
            bytes([OP_EQUALVERIFY, OP_SWAP]),
            push_int(3),
            bytes(
                [
                    OP_ROLL,
                    OP_SWAP,
                    OP_CAT,
                    OP_CAT,
                    OP_FROMALTSTACK,
                    OP_FROMALTSTACK,
                    OP_2DUP,
                    OP_EQUAL,
                    OP_NOT,
                    OP_VERIFY,
                    OP_2SWAP,
                    OP_FROMALTSTACK,
                    OP_CHECKSIGFROMSTACK,
                    OP_VERIFY,
                    OP_SWAP,
                    OP_DROP,
                    OP_CHECKSIGVERIFY,
                ]
            ),
            push_int(0),
            bytes([OP_OUTPUTHASH]),
            push_data(burn_output_hash),
            bytes([OP_EQUAL]),
        ]
    )


def serialize_txout(amount: int, script_pubkey: bytes) -> bytes:
    if amount < -0x8000000000000000 or amount > 0x7FFFFFFFFFFFFFFF:
        raise ValueError("amount does not fit int64")
    return struct.pack("<q", amount) + compact_size(len(script_pubkey)) + script_pubkey


def output_hash(amount: int, script_pubkey: bytes) -> bytes:
    return tagged_hash("OutputHash", serialize_txout(amount, script_pubkey))


def tapleaf_hash(script: bytes, leaf_version: int = TAPSCRIPT_LEAF_VERSION) -> bytes:
    return tagged_hash("TapLeaf", bytes([leaf_version]) + compact_size(len(script)) + script)


def tapbranch_hash(left: bytes, right: bytes) -> bytes:
    require_length("left", left, 32)
    require_length("right", right, 32)
    low, high = sorted((left, right))
    return tagged_hash("TapBranch", low + high)


def build_vectors() -> dict[str, Any]:
    alice = bytes.fromhex("79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798")
    user1 = bytes.fromhex("c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5")
    user2 = bytes.fromhex("f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9")
    stake_sid = bytes.fromhex("11" * 32)
    second_sid = bytes.fromhex("44" * 32)
    pid = bytes.fromhex("22" * 32)
    expiry = 500000
    burn_amount = 80000
    burn_script_pubkey = bytes.fromhex("6a05534c415348")
    burn_hash = output_hash(burn_amount, burn_script_pubkey)

    payment = payment_script(alice, pid)
    expiry_leaf = expiry_script(alice, expiry)
    slash = slash_script(alice, stake_sid, burn_hash)
    payment_leaf_hash = tapleaf_hash(payment)
    expiry_leaf_hash = tapleaf_hash(expiry_leaf)
    slash_leaf_hash = tapleaf_hash(slash)

    return {
        "specification": "UIP-3",
        "version": 1,
        "parameters": {
            "alice_pubkey": alice.hex(),
            "user1_pubkey": user1.hex(),
            "user2_pubkey": user2.hex(),
            "stake_sid": stake_sid.hex(),
            "second_sid": second_sid.hex(),
            "pid": pid.hex(),
            "expiry": expiry,
            "nums_internal_key": NUMS_INTERNAL_KEY.hex(),
            "burn_output": {
                "amount": burn_amount,
                "script_pub_key": burn_script_pubkey.hex(),
                "serialized_output": serialize_txout(burn_amount, burn_script_pubkey).hex(),
                "output_hash": burn_hash.hex(),
            },
        },
        "templates": {
            "payment": {
                "script": payment.hex(),
                "tapleaf_hash": payment_leaf_hash.hex(),
                "merkle_root": payment_leaf_hash.hex(),
            },
            "expiry": {
                "script": expiry_leaf.hex(),
                "tapleaf_hash": expiry_leaf_hash.hex(),
            },
            "slash": {
                "script": slash.hex(),
                "tapleaf_hash": slash_leaf_hash.hex(),
            },
            "stake_tree": {
                "merkle_root": tapbranch_hash(expiry_leaf_hash, slash_leaf_hash).hex(),
            },
        },
        "claims": {
            "claim1_message": (stake_sid + pid + user1).hex(),
            "claim1_signature": "e271b6599c211168bc07ba3f1deef27eacd39c674409093a12a8820887eac423e24f4006ecec1666c473d68edb011442eeb41b494ff0d806c823fa35c52edbac",
            "claim2_message": (second_sid + pid + user2).hex(),
            "claim2_signature": "d8aba28585e2579efe8449336c5f51f71e74ac006c79be17614afc0441c53568b7c8b14b9ecb68adb040a01bcee3133342fc5b4ce225da016697a91e449db966",
        },
        "witness_order": {
            "payment_bottom_to_top": [
                "recipient_transaction_signature",
                "alice_transaction_signature",
                "alice_claim_signature",
                "sid",
                "recipient_pubkey",
            ],
            "slash_bottom_to_top": [
                "user1_transaction_signature",
                "pid",
                "claim2_signature",
                "sid2",
                "user2_pubkey",
                "claim1_signature",
                "user1_pubkey",
            ],
            "expiry_bottom_to_top": ["alice_transaction_signature"],
        },
    }


def self_test() -> None:
    vectors = build_vectors()
    burn = vectors["parameters"]["burn_output"]
    assert burn["serialized_output"] == "8038010000000000076a05534c415348"
    assert burn["output_hash"] == "befec93f2d1e6035b100a7c3afa7cf555f16012d6cbe1494586436570892350e"
    assert len(bytes.fromhex(vectors["templates"]["payment"]["tapleaf_hash"])) == 32
    assert len(bytes.fromhex(vectors["templates"]["stake_tree"]["merkle_root"])) == 32
    assert len(bytes.fromhex(vectors["claims"]["claim1_message"])) == 96
    assert len(bytes.fromhex(vectors["claims"]["claim2_message"])) == 96
    checked_in_vectors = Path(__file__).with_name("template-test-vectors.json")
    if checked_in_vectors.exists():
        expected = json.loads(checked_in_vectors.read_text(encoding="utf-8"))
        assert vectors == expected, "checked-in test vectors do not match reference.py"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    self_test()
    if args.dump:
        print(json.dumps(build_vectors(), indent=2))
    elif not args.self_test:
        parser.print_help()


if __name__ == "__main__":
    main()
