import hashlib
import logging
import re
import warnings

import pytest

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # for Python 3.8

from data.bip39_vectors import VECTORS

from bipsea.bip32 import to_master_key
from bipsea.bip39 import (
    LANGUAGES,
    N_MNEMONICS,
    N_WORDS_META,
    entropy_to_words,
    to_master_seed,
    validate_mnemonic_words,
)
from bipsea.util import LOGGER, __app_name__

MNEMONIC_12 = {
    "words": [
        "noodle",
        "life",
        "devote",
        "warm",
        "sponsor",
        "truck",
        "ship",
        "safe",
        "race",
        "noble",
        "royal",
        "proof",
    ],
    "xprv": "xprv9s21ZrQH143K4CVjMYaXgM1o5Xi1EkZcUpckwUMbjHhpsmu8kAPVsM43S2J6FQw6kzd6noZTcFDtxXhQj7SZ6ix1t81itPJMdNfePGu9JCT",
    "tprv": "tprv8ZgxMBicQKsPf1jG27S2qzdnPf8DUGbcpNXsotn4DGCJfNeDjXjFP6RVMCTkFnKR8S9snuBDmbohRPF9rKnVunDcQmE2Yk2QYUR4q3gMjaR",
    "xpub": "xpub661MyMwAqRbcGgaCTa7Y3UxXdZYVeDHTr3YMjrmDHdEokaEHHhhkR9NXHHQ7Jjq9HK3xxpey7Jnsjx649ydXvTbXp2eyBzzz8HromKbw1PR",
    "tpub": "tpubD6NzVbkrYhZ4YUm3um6dFQHtxge9dbnXPg8f6QpMdXzhVrtzMvYqZb3MXKUtqEnP5DasaQAqeQcvS8afYqUmou3psdQGsXfDiFTDXJYhpKp",
}


logger = logging.getLogger(LOGGER)


@pytest.mark.parametrize("language, vectors", VECTORS.items(), ids=VECTORS.keys())
def test_vectors(language, vectors):
    for vector in vectors:
        entropy_str, mnemonic, seed, xprv = vector
        expected_words = re.split(r"\s+", mnemonic)
        expected_seed = bytes.fromhex(seed)

        computed_seed = to_master_seed(expected_words, passphrase="TREZOR")
        assert expected_seed == computed_seed
        # changing passphrase changes seed
        assert computed_seed != to_master_seed(expected_words, passphrase="TREZOr")

        entropy_bytes = bytes.fromhex(entropy_str)
        computed_xprv = to_master_key(expected_seed, mainnet=True, private=True)
        assert str(computed_xprv) == xprv

        with warnings.catch_warnings():
            # some test vectors are all 0 which we consider weak entropy
            if all(b == 0 for b in entropy_bytes):
                warnings.simplefilter("ignore")
            computed_words = entropy_to_words(
                len(expected_words), entropy_bytes, language
            )
        assert expected_words == computed_words
        assert validate_mnemonic_words(computed_words, language)


def test_meta():
    """Computed BIP-39 table with ENT, CS, ENT+CS"""
    for v in N_WORDS_META.values():
        assert (v["entropy_bits"] % 32) == 0, "Entropy bits must be a multiple of 32"
        assert (
            v["checksum_bits"] == v["entropy_bits"] // 32
        ), "Unexpected mismatch between checksum and entropy sizes"


def test_verify_checksum():
    correct = MNEMONIC_12["words"]
    assert validate_mnemonic_words(correct, "english")
    assert not validate_mnemonic_words(correct[:-1], "english")
    assert not validate_mnemonic_words(correct[:-1] + ["mix"], "english")


def test_test_main_pub_prv():
    for net in (True, False):
        for vis in (True, False):
            expected_type = {
                (True, True): "xprv",
                (True, False): "xpub",
                (False, True): "tprv",
                (False, False): "tpub",
            }[(net, vis)]
            seed = to_master_seed(MNEMONIC_12["words"], "")
            prv = str(to_master_key(seed, mainnet=net, private=vis))
            assert prv == MNEMONIC_12[expected_type]
            assert prv.startswith(expected_type)


@pytest.mark.parametrize("language", LANGUAGES.keys())
def test_wordlists(language):
    file_name = LANGUAGES[language]["file"]
    list_path = files(__app_name__) / "wordlists" / file_name
    with list_path.open("r") as f:
        raw = f.read()
    file_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    assert (
        file_hash == LANGUAGES[language]["hash"]
    ), f"unexpected contents in {file_name}"
    word_list = raw.splitlines()
    assert (
        len(word_list) == N_MNEMONICS == len(set(word_list))
    ), f"expected {N_MNEMONICS} unique words"
