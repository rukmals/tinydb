import hashlib
import json


def json_to_string(json_data):
    str_json = json.dumps(json_data, sort_keys=True).encode('utf8')
    return str_json

def two_jsons_hash(new_data, old_data):
    new_data_str = json_to_string(new_data)
    old_data_str = json_to_string(old_data)
    hash_str = new_data_str + old_data_str
    print(hash_str)
    h = hashlib.new('sha256')
    h.update(hash_str)
    print(h.hexdigest())
    return h.hexdigest()

new_data1 = {'name': 'Rukmal', 'age': 78}
old_data1 = {'name': 'Rukmal', 'age': 24}
new_data2 = {'name': 'Rukmal', 'age': 78}
old_data2 = {'name': 'Rukmal', 'age': 24}

two_jsons_hash(new_data1, old_data1)
two_jsons_hash(new_data2, old_data2)