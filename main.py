
from tinydb import TinyDB,where,Query
from tinydb.storages import MemoryStorage
from threading import Thread
import time



if __name__ == '__main__':
    db = TinyDB('database/db.json')
    User = Query()

    # print(db.insert({'name': 'John', 'age': 22}))
    # print(db.insert({'name': 'John', 'age': 37}))
    # print(db.insert({'name': 'Namal', 'age': 21}))
    # print(db.insert({'name': 'Rukmal', 'age': 25}))
    # print(db.insert({'name': 'Dinu', 'age': 26}))


    print(db.update({'age':35},User.name == 'Namal'))



    #print(db.remove(User.name=='Rukmal'))

