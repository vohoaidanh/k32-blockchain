# -*- coding: utf-8 -*-

import hashlib

from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP,OP_1, OP_0, OP_2, OP_HASH160, OP_EQUALVERIFY, OP_CHECKMULTISIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

SelectParams('testnet')

def create_txout(amount_to_send = 0.00001, destination_address = ''):
    txout = CMutableTxOut(amount_to_send*COIN, CBitcoinAddress(destination_address).to_scriptPubKey()) 
    return txout

# first key
h1 = hashlib.sha256(b'cost session limb library mansion burst note rule gallery trim ability danh').digest()
seckey1 = CBitcoinSecret.from_secret_bytes(h1)

# second key
h2 = hashlib.sha256(b'cost session limb library mansion burst note rule gallery trim ability huong').digest()
seckey2 = CBitcoinSecret.from_secret_bytes(h2)

# Create a redeemScript. Similar to a scriptPubKey the redeemScript must be
# satisfied for the funds to be spent.
redeem_script = CScript([OP_2, seckey1.pub, seckey2.pub, OP_2, OP_CHECKMULTISIG])

# Create the magic P2SH scriptPubKey format from that redeemScript. You should
# look at the CScript.to_p2sh_scriptPubKey() function in bitcoin.core.script to
# understand what's happening, as well as read BIP16:
# https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki
script_pubkey = redeem_script.to_p2sh_scriptPubKey()

# Convert the P2SH scriptPubKey to a base58 Bitcoin address and print it.
# You'll need to send some funds to it to create a txout to spend.

address = CBitcoinAddress.from_scriptPubKey(script_pubkey)

print('Address:',str(address))

print(50*'=')
print("Private Key 1:", seckey1)
print("Public Key 1: {0}".format(seckey1.pub.hex()))
print("Private Key 2:", seckey2)
print("Public Key 2: {0}".format(seckey2.pub.hex()))
print("Bitcoin Address:", address)
print(50*'=')

# we are continuing the code from above

txid = lx("0f813fd266eaaf97dd0465cf4ccbf784538c1f1d993cddb7066580c63ef1adec")
vout = 0



amount = COIN * 0.00001

# Create the txin structure, which includes the outpoint. The scriptSig defaults to being empty as
# is necessary for spending a P2WSH output.
txin = CMutableTxIn(COutPoint(txid, vout))

# Specify a destination address and create the txout.
destination = CBitcoinAddress('mhuL3JPyM7TmJ5PZHvu7V3YHeWZN8CD4MP').to_scriptPubKey() 

txout = CMutableTxOut(amount, destination)

# Create the unsigned transaction.
tx = CMutableTransaction([txin], [txout])


sighash = SignatureHash(
    script=redeem_script,
    txTo=tx,
    inIdx=0,
    hashtype=SIGHASH_ALL
)

# Now sign it. We have to append the type of signature we want to the end, in this case the usual
# SIGHASH_ALL.
sig1 = seckey1.sign(sighash) + bytes([SIGHASH_ALL])
sig2 = seckey2.sign(sighash) + bytes([SIGHASH_ALL])


# Construct a witness for this P2WSH transaction and add to tx.
txin.scriptSig = CScript([sig1, sig2, redeem_script])

#VerifyScript(txin.scriptSig, redeem_script, tx, 0, (SCRIPT_VERIFY_P2SH,))


# Done! Print the transaction
print(b2x(tx.serialize()))
# outputs: 0100000001d064760bbdf3c191c18e870a20bc6aabbc956caa7d32e5ad7f5907f3ebcda75500000000db00483045022100a22bf0495398d87538bb07daf62948572def31d411df6048e92a53b00d35f06c02204583f20a0fcbb6f5a978f32dde6dfadfe11581973eef946bb87e1ce5b164fb3a014830450221008611aacb5ab9efb1f64200800ac8f55bb6a1acbcdaa2d3db7741df6b99c9f6f802202be1a1c4fdcb649f622b25ad88befba4ef23689e07409bffd4a1d63237993dbd01475221038d19497c3922b807c91b829d6873ae5bfa2ae500f3237100265a302fdce87b052103d3a9dff5a0bb0267f19a9ee1c374901c39045fbe041c1c168d4da4ce0112595552aeffffffff01c09ee605000000001600147829e2df6fd013aa5303d4e0af578d4275629bd300000000









