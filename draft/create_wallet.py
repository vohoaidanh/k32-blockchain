# -*- coding: utf-8 -*-

from bitcoinlib.wallets import Wallet

wallet = Wallet('mywallet')

wallet.info()


wallet.get_keys()

from bitcoinlib.keys import HDKey
k = HDKey(witness_type='segwit')
k.info()

extended_wif = 'zprvAWgYBBk7JR8GkeJjDSwjSRVzELayEiGSBJnYoQDqhpLFThwUdiAvL9FbDuz66LexZrtAuh54iMqfEk7UgkqR7tghqdUDRQRzfhi5rG2HDVZ'

k = HDKey(extended_wif)
ck = k.child_private(10)
print("ck.private_hex: %s" % ck.private_hex)
ck_pub = ck.child_public(0)
print("ck_pub.private_hex: %s" % ck_pub.private_hex)
print("ck_pub.public_hex: %s" % ck_pub.public_hex)
print("ck_pub.depth: %s" % ck_pub.depth)

from bitcoinlib.keys import Address
address = 'bc1qrjnn8y0tlxzu3qcsz0jzeg5xggef3s7ef237d9'
a = Address.import_address(address)
print(a.as_json())


k.address(encoding='bech32')


