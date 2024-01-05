# -*- coding: utf-8 -*-

import hashlib

from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript,OP_CHECKSIG, OP_DUP, OP_EQUAL ,OP_1, OP_0, OP_2, OP_HASH160, OP_EQUALVERIFY, OP_CHECKMULTISIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2SHBitcoinAddress

SelectParams('testnet')

def create_txin(txid, output_index):
    _txid =  lx(txid) # Transaction ID of the UTXO you want to spend
    return CMutableTxIn(COutPoint(_txid, output_index))

def create_txout(amount = 0.00001, destination = ''):
    
    txout = CMutableTxOut(int(amount*COIN), CBitcoinAddress(destination).to_scriptPubKey()) 

    return txout

# first key
h1 = hashlib.sha256(b'cost session limb library mansion burst note rule gallery trim ability mot').digest()
seckey1 = CBitcoinSecret.from_secret_bytes(h1)

# second key
h2 = hashlib.sha256(b'cost session limb library mansion burst note rule gallery trim ability hai').digest()
seckey2 = CBitcoinSecret.from_secret_bytes(h2)

# Create redeem script -> multisig 
redeem_script = CScript([OP_2, seckey1.pub, seckey2.pub, OP_2, OP_CHECKMULTISIG])
script_pubkey = redeem_script.to_p2sh_scriptPubKey()

# Create bitcoin address from script_pubkey
address = CBitcoinAddress.from_scriptPubKey(script_pubkey)

txid = '52b1ee0246c0053a2ba1201518d5761b172b9968d0eac49079fc1fb91a0a052c'
vout = 0

# Create the txin structure, which includes the outpoint. The scriptSig defaults to being empty as

txin = create_txin(txid, vout)

# Specify a destination address and create the txout.
destination = 'mhuL3JPyM7TmJ5PZHvu7V3YHeWZN8CD4MP'

# Create txout
amount = 0.00001 
txout = create_txout(amount, destination)

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

print(50*'=')
print("Private Key 1:", seckey1)
print("Public Key 1: {0}".format(seckey1.pub.hex()))
print("Private Key 2:", seckey2)
print("Public Key 2: {0}".format(seckey2.pub.hex()))
print("Bitcoin Address:", address)
print("Amount to send in BTC ", amount)
print(50*'=')

print('Transaction raw data, we used this data to boardcast.')
print(50*'=')
print(b2x(tx.serialize()))
print(50*'=')

