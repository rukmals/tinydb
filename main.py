
from tinydb import TinyDB,where,Query
from tinydb.storages import MemoryStorage
from threading import Thread
import time
from blockchain.blockchain import Blockchain

def get_chain(blockchain):
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    print("chain data-----------------------------")
    for cd in chain_data:
        print(cd)


if __name__ == '__main__':
    db = TinyDB('database/db.json')
    User = Query()
    blockchains = Blockchain()

    # print(db.insert({'name': 'John', 'age': 22}))
    # print(db.insert({'name': 'John', 'age': 37}))
    # print(db.insert({'name': 'Namal', 'age': 21}))
    db.insert({'name': 'Rukmal', 'age': 25})
    # print(db.insert({'name': 'Dinu', 'age': 26}))
    get_chain(blockchains)

    db.update({'age':85},User.name == 'Namal')
    db.update({'age':23},User.name == 'Rukmal')
    blockchains.mine()

    db.update({'age':45},User.name == 'Namal')
    db.update({'age':12},User.name == 'Namal')
    db.update({'age':78},User.name == 'Rukmal')
    blockchains.mine()

    db.update({'age':34},User.name == 'John')
    db.update({'age':43},User.name == 'Namal')
    blockchains.mine()

    db.update({'age':56},User.name == 'Rukmal')
    db.update({'age':23},User.name == 'John')
    blockchains.mine()

    get_chain(blockchains)




