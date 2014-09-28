# -*- coding: utf-8 -*-
"""
    indexer
    ~~~~~~~~~~~~~~

    Information retrieval
    Computer Science Center, 2014


    :copyright: (c) 2014 by Elizaveta Shashkova.
"""

import sys
import re
from os import listdir
from os.path import isfile, join


class Indexer:
    def __init__(self, path, output):
        self.files_path = path
        self.output = output
        self.indexes = {}
        self.files = []


    def _process_line(self, line, file_num):
        p = re.compile("\{([а-я\|]+)\}")
        lex_in_file = p.findall(line)
        for lex in lex_in_file:
            words = lex.split('|')
            for word in words:
                if word not in self.indexes:
                    self.indexes[word] = []
                if file_num not in self.indexes[word]:
                    self.indexes[word].append(file_num)


    def _create_file_index(self, path, file_num):
        file = open(path)
        for line in file:
            self._process_line(line.rstrip(), file_num)


    def create_index(self):
        files = [join(self.files_path, f) for f in listdir(self.files_path) if isfile(join(self.files_path, f))]
        self.files = files
        for file in files:
            file_num = files.index(file)
            self._create_file_index(file, file_num)


    def write_index_to_file(self):
        output_file = open(self.output, "w")
        for file in self.files:
            output_file.write(str(file) + '\t')
        output_file.write('\n')
        for k, v in self.indexes.items():
            output_file.write(k + ':')
            for word_files in v:
                output_file.write(str(word_files) + '\t')
            output_file.write('\n')
        output_file.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: path with documents and name of output file")
    else:
        indexer = Indexer(sys.argv[1], sys.argv[2])
        indexer.create_index()
        #print(indexer.indexes)
        indexer.write_index_to_file()