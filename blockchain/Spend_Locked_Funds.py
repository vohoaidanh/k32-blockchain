# -*- coding: utf-8 -*-

# Spend Locked Funds
from bitcoin import *

from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL, OP_0
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress
SelectParams('testnet')


def create_txin(txid, output_index):
    txid = lx(txid) # Transaction ID of the UTXO you want to spend
    return CMutableTxIn(COutPoint(txid, output_index))

def create_txout(amount_to_send = 0.00001, destination_address = ''):
    txout = CMutableTxOut(amount_to_send*COIN, CBitcoinAddress(destination_address).to_scriptPubKey()) 
    return txout

def signed_transaction(tx, private_key):
        
    # Calculate the signature hash for that transaction.
    
    txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(private_key.pub), OP_EQUALVERIFY, OP_CHECKSIG])
    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)
    
    # Now sign it. We have to append the type of signature we want to the end, in
    # this case the usual SIGHASH_ALL.
    sig = private_key.sign(sighash) + bytes([SIGHASH_ALL])
    
    # Set the scriptSig of our transaction input appropriately.
    tx.vin[0].scriptSig = CScript([sig, private_key.pub])
    
    # Verify the signature worked. This calls EvalScript() and actually executes
    # the opcodes in the scripts to see if everything worked out. If it doesn't an
    # exception will be raised.
    VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))
    #Return raw value ready to boarcast
    return tx.serialize().hex()

SelectParams('testnet')

# Private key and Bitcoin address from the previous step (we had created in P2PKH_Script.py)
private_key = CBitcoinSecret('cN5rJPxSoLCUd53GT8W27X7EdGJx1dopFcCEnZHFDSFgPnmC31Rh')

# Bitcoin Address we had created in P2PKH_Script.py
address = P2PKHBitcoinAddress('mhuL3JPyM7TmJ5PZHvu7V3YHeWZN8CD4MP')

# Create a transaction input (UTXO)

#txid = 'a9f14fa5ddd8310556b18418aeeaa3edb92ee9eae151d0d3a7d651190c351c20' # Transaction ID of the UTXO you want to spend
txid = 'ad301f20e72e867c0853119ece9cb7daf3e79e29d9bc17a6571b943a213a7040'
output_index = 0 # Index of the output in the transaction
txin = create_txin(txid, output_index)

# Create a transaction output to the desired destination

destination_address = 'tb1q6sudyq4d9ejaykpkeqgv4pxcdthzdr2yxanhzc' # Recipient’s address
amount_to_send = 0.00001 # Amount to send in satoshis
txout = create_txout(amount_to_send,destination_address)

# Create the transaction (unsigned).
tx = CMutableTransaction([txin], [txout])

# Sign this transaction

raw_transaction = signed_transaction(tx, private_key)

print(50*'=')
print('Transaction infomation')
print("Private Key:", private_key)
print("Bitcoin Address:", address)
print("Destination address: ", destination_address)
print("Amount to send in satoshis ", amount_to_send*COIN)

print(50*'=')
print('Transaction raw data, we used this data to boardcast.')
print(50*'=')
print(b2x(tx.serialize()))
print(50*'=')


