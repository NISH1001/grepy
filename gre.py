#!/usr/bin/env python3

import os
import json
import random
import time
import datetime

def get_abs_path(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path, filename)

def load_words(filename):
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

def read_todays_words(filename):
    words = []
    ts = time.time()
    date_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    filename = get_abs_path(filename)
    with open(filename) as f:
        timestamp = float(f.readline().strip())
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        if date == date_today:
            for line in f:
                words.append(line.strip())
    return set(words)

def save_todays_words(filename, words):
    ts = time.time()
    date_today = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    filename = get_abs_path(filename)
    with open(filename, 'r') as f:
        timestamp = float(f.readline().strip())
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        if date == date_today:
            return
    with open(filename, 'w') as f:
        f.write("{}\n".format(time.time()))
        for word in words:
            f.write("{}\n".format(word))

def save_used_words(filename, words):
    all_used_words = get_used_words(filename)
    words = all_used_words.union(words)
    filename = get_abs_path(filename)
    with open(filename, 'w') as f:
        for word in words:
            f.write("{}\n".format(word))

def get_used_words(filename):
    res = []
    filename = get_abs_path(filename)
    with open(filename) as f:
        for line in f:
            res.append(line.strip())
    return set(res)

def get_todays_words(word_map, used_words, filename_today, n=5):
    # save_todays_words(filename_today, used_words)
    todays_words = read_todays_words(filename_today)
    if not todays_words:
        wmap = get_random_words(word_map, used_words, n)
        todays_words = set(wmap.keys())
    return { word : word_map[word] for word in todays_words }


def main():
    word_map = load_words('data/vocab-list.txt')

    used_words = get_used_words('data/used-words')
    wmap = get_todays_words(word_map, used_words, 'data/today-words')
    save_used_words('data/used-words', set(wmap.keys()))
    save_todays_words('data/today-words', set(wmap.keys()))

    print('-'*100)
    print("Words for Today")
    print('-'*100)
    for word in wmap:
        print("{} ::: {}".format(word, wmap[word]))
    print('-'*100)


if __name__ == "__main__":
    main()

