#!/usr/bin/env python3

import os
import json
import random
import time
import datetime

def get_abs_path(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path, filename)

def load_vocabs(filename):
    word_map = {}
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path, filename)
    with open(filename) as f:
        for line in f:
            tokens = line.split('-')
            word = tokens[0].strip()
            meaning = tokens[1].strip()
            word_map[word] = meaning
    return word_map


def get_random_words(word_map, used_words, n=5):
    all_words = set(word_map.keys())
    remaining_words = all_words - used_words
    words = random.sample(remaining_words, n)
    return {word : word_map[word] for word in words }

def get_todays_words(word_map, used_map, n=5):
    ts = time.time()
    date_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d').strip()
    used_words = set([ word for words in used_map.values() for word in words ])
    if date_today not in used_map :
        wmap = get_random_words(word_map, used_words, n)
    else:
        words = used_map[date_today]
        wmap = { word : word_map[word] for word in words }
    used_map[date_today] = list(set(wmap.keys()))
    return wmap, used_map

def load_used_map(filename):
    filename = get_abs_path(filename)
    try:
        with open(filename) as f:
            used_map = json.load(f)
            return used_map if used_map else {}
    except FileNotFoundError:
        with open(filename, 'w') as f:
            json.dump({}, f,)
            return {}

def save_used_map(filename, used_map):
    filename = get_abs_path(filename)
    with open(filename, 'w') as f:
        json.dump(used_map, f, indent=4)

def main():
    word_map = load_vocabs('data/vocab-list.txt')
    used_map = load_used_map('data/used-map.json')
    wmap, used_map = get_todays_words(word_map, used_map, n=5)
    save_used_map('data/used-map.json', used_map)
    print('-'*100)
    print("Words for Today")
    print('-'*100)
    for word in wmap:
        print("{} ::: {}".format(word, wmap[word]))
    print('-'*100)


if __name__ == "__main__":
    main()
