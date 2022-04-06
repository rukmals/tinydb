
from tinydb import TinyDB,where,Query
from tinydb.storages import MemoryStorage
from threading import Thread
import time
from blockchain.blockchain import Blockchain



if __name__ == '__main__':
    db = TinyDB('database/db.json')
    User = Query()

    # print(db.insert({'name': 'John', 'age': 22}))
    # print(db.insert({'name': 'John', 'age': 37}))
    # print(db.insert({'name': 'Namal', 'age': 21}))
    db.insert({'name': 'Rukmal', 'age': 25})
    # print(db.insert({'name': 'Dinu', 'age': 26}))
    print(Blockchain.chain)

    db.update({'age':85},User.name == 'Namal')
    db.update({'age':23},User.name == 'Rukmal')
    Blockchain.mine()

    db.update({'age':45},User.name == 'Namal')
    db.update({'age':12},User.name == 'Namal')
    db.update({'age':78},User.name == 'Rukmal')
    Blockchain.mine()

    db.update({'age':34},User.name == 'John')
    db.update({'age':43},User.name == 'Namal')
    Blockchain.mine()

    db.update({'age':56},User.name == 'Rukmal')
    db.update({'age':23},User.name == 'John')
    Blockchain.mine()



