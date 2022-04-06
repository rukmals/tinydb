import time
import json
from blockchain.block import Block
from blockchain.transaction import Transaction, TransactionEncoder


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

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def new_block_transactions(self):
        new_transactions = []
        print("length", str(len(self.last_block.transactions)))
        if len(self.last_block.transactions) < 1:
            last_transaction_id = 0
        else:
            print(self.last_block.transactions)
            last_transaction_id = json.JSONDecoder().decode(self.last_block.transactions[-1])['transaction_id']


            # read from db_transactions
        with open("/home/nuwanga/projects/tinydb/database/db_transactions.json", 'r+') as file:
            file_data = json.load(file)
            for d in file_data["_default"]:
                if last_transaction_id < d['transaction_id']:
                    transaction = Transaction(d['transaction_id'], d['user'], d['time_stamp'], d['hash'])
                    new_transactions.append(TransactionEncoder().encode(transaction))

        return new_transactions

    def mine(self):
        new_transactions = self.new_block_transactions()
        print(new_transactions)
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
