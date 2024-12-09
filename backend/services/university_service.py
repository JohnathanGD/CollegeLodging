import json
from backend.services.trie import Trie
import os

UNIVERSITY_DATASET_PATH = os.path.join(os.path.dirname(__file__), '../data/us-colleges-and-universities.json')

with open(UNIVERSITY_DATASET_PATH) as f:
    university_data = json.load(f)

university_index = {}
trie = Trie()

for uni in university_data:
    name = uni['name'].lower()
    alias = uni.get('alias', '').lower()
    state = uni['state'].lower()
    city = uni['city'].lower()
    zip_code = uni['zip'].lower()

    university_index[(name, 'name')] = uni
    if alias:
        university_index[(alias, 'alias')] = uni
    if state:
        if (state, 'state') not in university_index:
            university_index[(state, 'state')] = []
        university_index[(state, 'state')].append(uni)
    if city:
        if (city, 'city') not in university_index:
            university_index[(city, 'city')] = []
        university_index[(city, 'city')].append(uni)
    if zip_code:
        if (zip_code, 'zip') not in university_index:
            university_index[(zip_code, 'zip')] = []
        university_index[(zip_code, 'zip')].append(uni)

    trie.insert(name, uni)
    if alias:
        trie.insert(alias, uni)

def get_university_data_by_key(key, key_type):
    return university_index.get((key.lower(), key_type))

def get_university_data_by_name(name):
    return university_index.get((name.lower(), 'name'))

def get_university_data_by_alias(alias):
    return university_index.get((alias.lower(), 'alias'))

def get_university_by_name_or_alias(name):
    return get_university_data_by_name(name) or get_university_data_by_alias(name)

def get_university_data_by_state(state):
    return university_index.get((state.lower(), 'state'), [])

def get_university_data_by_city(city):
    return university_index.get((city.lower(), 'city'), [])

def get_university_data_by_zipcode(zip_code):
    return university_index.get((zip_code.lower(), 'zip'), [])

def get_university_data_by_prefix(prefix):
    return trie.search(prefix.lower())