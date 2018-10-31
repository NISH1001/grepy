#!/usr/bin/env python3

import os


def merge_vocabs(*filenames):
    r = {}
    for filename in filenames:
        print(filename)
        with open(filename) as f:
            word_map = {}
            for line in f:
                tokens = line.split('-')
                word = tokens[0].strip()
                meaning = tokens[1].strip()
                word_map[word] = meaning
        r.update(word_map)
    return r



def main():
    wmap = merge_vocabs('data/vocab-list-1.txt', 'data/vocab-list-2.txt')
    with open('data/vocab-list.txt', 'w') as f:
        for word in wmap:
            meaning = wmap[word]
            f.write("{} - {}\n".format(word, meaning))

if __name__ == "__main__":
    main()

