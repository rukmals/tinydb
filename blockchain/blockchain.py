import hashlib
import time
import json
from blockchain.block import Block
from blockchain.transaction import Transaction, TransactionEncoder
from tinydb.table import Table



class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    difficulty = 2

    def proof_of_work(self, block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    # def add_new_transaction(self, transaction):
    #     self.unconfirmed_transactions.append(transaction)

    def new_block_transactions(self):
        new_transactions = []
        # print("length", str(len(self.last_block.transactions)))
        if len(self.last_block.transactions) < 1:
            last_transaction_id = 0
        else:
            # print(self.last_block.transactions)
            last_transaction_id = json.JSONDecoder().decode(self.last_block.transactions[-1])['transaction_id']


            # read from db_transactions
        with open("database/db_transactions.json", 'r+') as file:
            file_data = json.load(file)
            for d in file_data["_default"]:
                if last_transaction_id < d['transaction_id']:
                    transaction = Transaction(d['transaction_id'], d['user'], d['time_stamp'], d['hash'])
                    new_transactions.append(TransactionEncoder().encode(transaction))

        return new_transactions

    def mine(self):
        new_transactions = self.new_block_transactions()
        # print(new_transactions)
        if not new_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=new_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        return new_block.index

    def verify(self, index):
        chain_data = self.get_chain()
        if len(chain_data) < index + 1:
            index = len(chain_data) - 1

        for idx in range (0,index + 1):
            block = chain_data[idx]
            if len(block['transactions']) == 0:
                continue
            else:
                for trans in block['transactions']:
                    decoded_trans = json.JSONDecoder().decode(trans)
                    trans_id = decoded_trans['transaction_id']
                    print(trans_id)
                    hash_value = decoded_trans['hash']
                    print(hash_value)
                    reconstructed_hash_value = self.reconstruct_hash(trans_id)
                    print(reconstructed_hash_value)

                    if hash_value == reconstructed_hash_value:
                        continue
                    else:
                        print("false")
                        return False
        print('true')
        return True

    def reconstruct_hash(self,trans_id):
        #read from db_history
        obj_hdb = json.load(open("database/db_history.json"))
        documents = obj_hdb['_default']
        for raw in documents:
            found = False
            for key, value in raw.items():

                value_length = len(value)
                idx =  0
                for entry in value:
                    idx = idx + 1
                    if entry['trans_id'] == trans_id:
                        doc_id = key
                        old_data = entry['data']
                        found = True
                        operation = entry['operation']
                        break
                if found:
                    if idx == value_length:
                        if operation == "DELETE":
                            new_data = ''
                        else:
                            # read from db_history
                            obj_db = json.load(open("database/db.json"))
                            db_documents = obj_db['_default']
                            new_data = db_documents[str(doc_id)]
                    else:
                        new_data = value[idx]['data']



        # print(old_data)
        # print(new_data)
        hash_value = self.two_jsons_hash(new_data, old_data)
        # print(hash_value)
        return hash_value

    def json_to_string(self, json_data):
        str_json = json.dumps(json_data, sort_keys=True).encode('utf8')
        return str_json

    def two_jsons_hash(self,new_data,old_data):
        new_data_str = self.json_to_string(new_data)
        old_data_str = self.json_to_string(old_data)
        hash_str = new_data_str + old_data_str
        # print(hash_str)
        h = hashlib.new('sha256')
        h.update(hash_str)
        return h.hexdigest()

    def get_chain(self):
        chain_data = []
        for block in self.chain:
            chain_data.append(block.__dict__)
        return chain_data