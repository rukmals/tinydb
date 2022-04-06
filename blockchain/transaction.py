import json
from json import JSONEncoder


class Transaction:
    """
    Transaction: a class that represents a transaction.
    """

    def __init__(self, transaction_id, user, timestamp, hash):
        self.transaction_id = transaction_id
        self.user = user
        self.timestamp = timestamp
        self.hash = hash


class TransactionEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

# class TransactionDecoder():

