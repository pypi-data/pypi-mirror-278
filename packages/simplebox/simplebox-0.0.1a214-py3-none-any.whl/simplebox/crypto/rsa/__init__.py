#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pathlib import Path
from typing import Union

from Crypto import Random
from Crypto.PublicKey import RSA

from ._rsa import RsaEncrypt, RsaDecrypt, DigestAlgorithm

__all__ = ['generator_key', 'read_key',
           RsaEncrypt, RsaDecrypt, DigestAlgorithm]

_random_generator = Random.new().read


def generator_key(length=2048, output=None, suffix='key') -> Union[tuple[bytes, bytes]]:
    """
    generator private key and public key
    :param length: The length of the key
    :param output: save private/public key to file, this is a dir.
    :param suffix: output file suffix, default prefix is 'rsa_xxx_'
    :return: (private key, public key)
    """
    rsa = RSA.generate(length, _random_generator)
    private = rsa.export_key()
    public = rsa.public_key().export_key()
    if output:
        root = Path(output)
        private_file = root.joinpath(f"rsa_private_{suffix}.pem")
        public_file = root.joinpath(f"rsa_public_{suffix}.pem")
        if not root.exists():
            raise FileNotFoundError(f"'{root}' not found.")
        with open(private_file, 'wb') as f:
            f.write(private)
        with open(public_file, 'wb') as f:
            f.write(public)
    return private, public


def read_key(file) -> bytes:
    p = Path(file)
    if not p.exists():
        raise FileNotFoundError(f"'{file}' not found.")
    with open(p, 'rb') as f:
        return f.read()
