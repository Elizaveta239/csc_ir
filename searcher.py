# -*- coding: utf-8 -*-
"""
    searcher
    ~~~~~~~~~~~~~~

    Information retrieval
    Computer Science Center, 2014


    :copyright: (c) 2014 by Elizaveta Shashkova.
"""
import sys


class Searcher:
    def __init__(self, indexes_path):
        self.indexes_path = indexes_path
        self.files = []
        self.indexes = {}


    def read_indexes(self):
        file = open(self.indexes_path)
        line = file.readline().rstrip()
        self.files = line.split('\t')
        for line in file:
            word_ind = line.rstrip().split(':')
            word = word_ind[0]
            files_num = [int(ind) for ind in word_ind[1].split('\t')]
            self.indexes[word] = files_num


    def query_and(self, words):
        answer_files = set(range(len(self.files)))
        for word in words:
            if word not in self.indexes:
                answer_files = {}
                break
            answer_files = set(self.indexes[word]).intersection(answer_files)
        print(answer_files)


    def query_or(self, words):
        answer_files = set()
        for word in words:
            if word in self.indexes:
                set(self.indexes[word]).union(answer_files)
        print(answer_files)


    def process_queries(self):
        for line in sys.stdin:
            query = line.rstrip()
            if 'AND' in query:
                words = [word.strip() for word in query.split('AND')]
                self.query_and(words)
            elif 'OR' in query:
                words = [word.strip() for word in query.split('OR')]
                self.query_or(words)
            else:
                words = [query.strip()]
                self.query_and(words)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: path with indexes")
    else:
        searcher = Searcher(sys.argv[1])
        searcher.read_indexes()
        #print(searcher.indexes)
        searcher.process_queries()