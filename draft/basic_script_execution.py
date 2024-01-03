# -*- coding: utf-8 -*-
import os
# P2PKH Script
from bitcoin import *
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoinlib.keys import Key
# Generate a random private key

# Derive the public key and Bitcoin address

k = Key(network='testnet')
print(k.address())
print(k.address(encoding='bech32'))


k = Key()
k.info()

from bitcoinlib.keys import Key

k = Key(import_key='033074179f5ff489fc099cf8a06227367b60fa25eccaae01f43660f1d234c1b91d',
        network='testnet')
k.address(encoding='bech32')

