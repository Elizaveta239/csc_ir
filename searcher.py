#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
    searcher
    ~~~~~~~~~~~~~~

    Information retrieval
    Computer Science Center, 2014


    :copyright: (c) 2014 by Elizaveta Shashkova.
"""
import re
import sys
from pickle import Unpickler


class Searcher:
    def __init__(self, indexes_path):
        self.indexes_path = indexes_path
        self.files = []
        self.indexes = {}

    def read_indexes(self):
        unpickler = Unpickler(open(self.indexes_path, "rb"))
        self.files = unpickler.load()
        self.indexes = unpickler.load()

    def query_and(self, words):
        answer_files = set(range(len(self.files)))
        for word in words:
            if word not in self.indexes:
                answer_files = {}
                break
            answer_files = set(self.indexes[word]).intersection(answer_files)
        return answer_files

    def query_or(self, words):
        answer_files = set()
        for word in words:
            if word in self.indexes:
                answer_files = set(self.indexes[word]).union(answer_files)
        return answer_files

    def show_answer(self, answer):
        answer_names = [self.files[file_id] for file_id in answer]
        if len(answer_names) == 0:
            print('no documents found')
        elif 0 < len(answer_names) <= 2:
            ans = 'found '
            for file_name in answer_names:
                ans += ' ' + file_name
            print(ans)
        elif len(answer_names) > 2:
            ans = 'found '
            ans = ans + answer_names[0] + ' '
            ans = ans + answer_names[1] + ' '
            ans += 'and %d more' % (len(answer_names) - 2)
            print(ans)

    def is_correct_query(self, query):
        p = re.compile("^[а-я]+( AND [а-я]+)*$")
        if p.match(query):
            return True
        p = re.compile("^[а-я]+( OR [а-я]+)*$")
        if p.match(query):
            return True
        return False

    def process_queries(self):
        for line in sys.stdin:
            query = line.strip()
            if not self.is_correct_query(query):
                print('incorrect query')
                continue

            if 'AND' in query:
                words = [word.strip() for word in query.split('AND')]
                answer = self.query_and(words)
            elif 'OR' in query:
                words = [word.strip() for word in query.split('OR')]
                answer = self.query_or(words)
            else:
                words = [query.strip()]
                answer = self.query_and(words)

            self.show_answer(answer)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: path with indexes")
    else:
        searcher = Searcher(sys.argv[1])
        searcher.read_indexes()
        searcher.process_queries()