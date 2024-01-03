# -*- coding: utf-8 -*-
import os
import hashlib
# P2PKH Script
from bitcoin import *
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

# For select testnet network setting
from bitcoin import SelectParams
SelectParams('testnet')

# Generate a  private key
# Tạo 32 byte hash từ 1 chuổi gợi nhớ để có thể khôi phục lại thông tin nếu chúng ta quên

h = hashlib.sha256(b'cost session limb library mansion burst note rule gallery trim ability forget').digest()
private_key = CBitcoinSecret.from_secret_bytes(h)
#private_key = CBitcoinSecret.from_secret_bytes(os.urandom(32))

# Derive the public key and Bitcoin address
public_key = private_key.pub
address = P2PKHBitcoinAddress.from_pubkey(public_key)

print(50*'=')
print("Private Key:", private_key)
print("Public Key: {0}".format(public_key.hex()))
print("Bitcoin Address:", address)
print(50*'=')


