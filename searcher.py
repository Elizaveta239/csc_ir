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
    QUERY_INCORRECT = -1
    QUERY_AND = 0
    QUERY_OR = 1
    QUERY_COORD = 2

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
            answer_files = set([pair[0] for pair in self.indexes[word]]).intersection(answer_files)
        return answer_files

    def query_or(self, words):
        answer_files = set()
        for word in words:
            if word in self.indexes:
                answer_files = set([pair[0] for pair in self.indexes[word]]).union(answer_files)
        return answer_files

    def coord_pair(self, word1, word2, dist):
        ans = set()
        for pair1 in self.indexes[word1]:
            for pair2 in self.indexes[word2]:
                if pair1[0] == pair2[0]:
                    if 0 <= pair2[1] - pair1[1] <= dist:
                        ans.add(pair1[0])
        return ans

    def query_coord(self, query):
        details = [word.strip() for word in query.split(' ')]
        answer_files = set(range(len(self.files)))
        for ind in range(0, len(details) - 2, 2):
            word1 = details[ind]
            word2 = details[ind + 2]
            distance = details[ind + 1][1:]
            double_side = False
            if distance[0] == "+":
                distance = distance[1:]
            elif distance[0] == "-":
                word1, word2 = word2, word1
                distance = distance[1:]
            else:
                double_side = True

            distance = int(distance)
            if not double_side:
                ans_pair = self.coord_pair(word1, word2, distance)
            else:
                ans_pair = self.coord_pair(word1, word2, distance). \
                    union(self.coord_pair(word2, word1, distance))
            answer_files = ans_pair.intersection(answer_files)
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
            return 0
        p = re.compile("^[а-я]+( OR [а-я]+)*$")
        if p.match(query):
            return 1
        p = re.compile("^[а-я]+( \/[\+\-]?[0-9]* [а-я]+)*$")
        if p.match(query):
            return 2
        return -1

    def process_queries(self):
        for line in sys.stdin:
            query = line.strip()
            is_correct = self.is_correct_query(query)
            if is_correct == self.QUERY_INCORRECT:
                print('incorrect query')
                continue
            elif is_correct == self.QUERY_AND:
                words = [word.strip() for word in query.split('AND')]
                answer = self.query_and(words)
            elif is_correct == self.QUERY_OR:
                words = [word.strip() for word in query.split('OR')]
                answer = self.query_or(words)
            elif is_correct == self.QUERY_COORD:
                answer = self.query_coord(query)

            self.show_answer(answer)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: path with indexes")
    else:
        searcher = Searcher(sys.argv[1])
        searcher.read_indexes()
        searcher.process_queries()