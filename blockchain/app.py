from flask import Flask,request
import requests
import json
from blockchain import Blockchain
from transaction import Transaction,TransactionEncoder
app = Flask(__name__)

blockchain =  Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/add', methods=['POST'])
def add_transaction():
    request_data = request.get_json()
    transaction = Transaction(request_data['transaction_id'],request_data['user'],request_data['timestamp'],request_data['hash'])
    blockchain.add_new_transaction(TransactionEncoder().encode(transaction))
    return "True"

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.mine()
    return "True"
app.run(debug=True, port=5000)
