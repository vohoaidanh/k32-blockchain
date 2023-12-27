
# coding: utf-8

from hashlib import sha256
import json
import time
from flask import Flask, render_template, request, jsonify
#import requests

def get_merkle_path(transactions, transId):
    """
    This function get the Merkle path from a special transaction ID
    """
    # Tạo merkle tree
    tree = build_merkle_tree(transactions)

    path = []
    index = transId #current Index transaction

    for level in range(len(tree)-1):
        sibling_index = index + 1 if index % 2 == 0 else index - 1
        path.append((sibling_index, tree[level][sibling_index]))
        index = index // 2  # Move to the parent node
    return path
        
def build_merkle_tree(transactions):
    """
    A function that builds the Merkle Tree and returns the list with earch element is contain hash of all leaf of same level.
    """
    if len(transactions) == 0:
        return sha256(b"").hexdigest()

    # Convert transactions to list of strings
    transaction_strings = [json.dumps(tx) for tx in transactions]

    # Build the Merkle Tree
    merkle_root = [sha256(tx.encode()).hexdigest() for tx in transaction_strings]
    tree = [merkle_root]
    while len(merkle_root) > 1:
        if len(merkle_root) % 2 == 1:
                merkle_root.append(merkle_root[-1])
        merkle_root = [sha256(merkle_root[i].encode() + merkle_root[i + 1].encode()).hexdigest() for i in range(0, len(merkle_root), 2)]
        tree.append(merkle_root)
    return tree

def verify_transaction(block, transId, transaction):
    transactions = block.transactions
    block_hash = block.hash
    tree = get_merkle_path(transactions, transId)
    merkle_root_hash = sha256(json.dumps(transaction).encode()).hexdigest()
    
    for i, tx in tree:
        if i%2 == 0:
            # Nếu Node trong Merkle path nằm bên trái.
            merkle_root_hash = sha256(tx.encode() + merkle_root_hash.encode()).hexdigest()
        else:
            merkle_root_hash = sha256(merkle_root_hash.encode() + tx.encode()).hexdigest()
            
    block_string = json.dumps({
        'timestamp' : block.timestamp, 
        'previous_hash': block.previous_hash, 
        'merkle_root_hash' : merkle_root_hash,
        'nonce': block.nonce
        }, sort_keys=True)
    
    reconstruct_hash = sha256(block_string.encode()).hexdigest()
    
    return block_hash==reconstruct_hash


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = None
        self.nonce = 0

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        merkle_root_hash = build_merkle_tree(self.transactions)[-1][0]
        block_string = json.dumps({
            'timestamp' : self.timestamp, 
            'previous_hash': self.previous_hash, 
            'merkle_root_hash' : merkle_root_hash,
            'nonce': self.nonce
            }, sort_keys=True)

        return sha256(block_string.encode()).hexdigest()


    
class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 1

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('01' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('01' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index
    
    def verify_transaction_in_block(self, transaction_hash, block_index):
        """
        A function to verify if a transaction belongs to a block using Merkle Tree.
        """
        if not self.is_valid_block_index(block_index):
            return False
    
        block = self.chain[block_index]
        merkle_root = block.build_merkle_tree_root(block.transactions)
    
        # Tính toán hash của giao dịch cần xác minh
        target_hash = sha256(transaction_hash.encode()).hexdigest()
    
        # Xác minh sự thuộc về của giao dịch trong cây Merkle
        return merkle_root == target_hash



# =============================================================================
# 
# chain = Blockchain()
# time.sleep(1)
# chain.add_new_transaction(transaction='Transaction 1')
# chain.add_new_transaction(transaction='Transaction 2')
# chain.mine()
# time.sleep(1)
# chain.add_new_transaction(transaction='Transaction 1')
# chain.add_new_transaction(transaction='Transaction 2')
# chain.add_new_transaction(transaction='Transaction 3')
# chain.add_new_transaction(transaction='Transaction 4')
# chain.add_new_transaction(transaction='Transaction 5')
# chain.add_new_transaction(transaction='Transaction 6')
# chain.add_new_transaction(transaction='Transaction 7')
# chain.add_new_transaction(transaction='Transaction 8')
# 
# 
# chain.mine()
# 
# chain.chain[-2].__dict__
# 
# verify_transaction(chain.chain[2],2,'Transaction 3')
# 
# b = chain.chain[2]
# b.build_merkle_tree_root(b.transactions)
# =============================================================================


app = Flask(__name__)

#app.run(debug=True, port=5000)

# Danh sách giao dịch và khối đơn giản (chỉ để mô phỏng)
chain = Blockchain()
transactions = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.form['transaction_data']
    transactions.append(data)
    return json.dumps({'satus': 'success', 'Transaction': transactions})
    #return jsonify({'status': 'success', 'message': 'Transaction added successfully'})


@app.route('/create_block', methods=['POST'])
def create_block():
    global transactions
    global chain
    for tx in transactions:        
        chain.add_new_transaction(tx)
    
  
    chain.mine()
    #Xóa transactions sau khi mine xong
    
    transactions = []
    return get_chain()
    
    #return jsonify({'status': 'success', 'message': 'Block created successfully', 'blockchain': blockchain})

def get_chain():
    chain_data = []
    for block in chain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/view_chain', methods=['POST'])
def get_block():
    blockId = ''
    try:
        blockId = request.form['blockId']
    except:
        blockId = ''
    
    chain_data = []
    if blockId != '':
        for block in chain.chain:
            if str(block.index) == str(blockId): 
                chain_data.append(block.__dict__)
    else:
        for block in chain.chain:
            chain_data.append(block.__dict__)
            
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/verify_transaction', methods=['POST'])
def verify():
    block_id = request.form.get('blockId')
    trans_id = request.form.get('transId')
    transaction = request.form.get('transaction')

    # Thực hiện xác minh giao dịch
    block = chain.chain[int(block_id)]
    result = verify_transaction(block, int(trans_id), transaction)
    
    if result:
        result = "Ok"
    else:
        result = "Verify not OK"

    # Đối với mục đích demo, trả về một JSON response
    response_data = {'result_verify': result}
    return jsonify(response_data)






   
