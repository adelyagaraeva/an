import sys

from backend.tree_visitors import *
from backend.metrics import *
from itertools import product
from print_color import print as print_color
from logging_ap.logging_app import my_logger


class Model:
    """
    Model accepts metrics and what you are parsing (python or not)
    and run one-by-one comparison of all files you give to it
    """

    def __init__(self, parse_python, metrics: list):
        my_logger.info("Initializing the model")
        self.parse_python = parse_python
        self.metrics = metrics
        self.suspects = {}

    def read_file(self, filename):
        """
        name: name of the file

        returns file as a string
        if not possible to read, and
        we do not compare python files,
        none is returned
        """
        my_logger.info("File reading")
        try:
            with open(filename, mode='r', encoding='utf8') as f:
                file = f.read()
        except UnicodeDecodeError as e:
            my_logger.error("trying to decode a string containing non-utf-8 characters")
            print_color(f'{e} in file {filename}', color='red')
            return None
        my_logger.info("File has been read successfully")
        return file

    def run(self, filenames_to_compare):
        """
        filenames_to_compare: filenames, not files itself
        files: you can also send files by themselves

        run one-by-one comparison of all files

        return: dictionary with all metrics for all comparisons of type
        (filename1, filename2) : [results for all metrics]
        """
        my_logger.info("Running the model")
        if self.parse_python:
            files_to_compare = {filename: self.preprocessing(filename)
                                for filename in filenames_to_compare}
        else:
            files_to_compare = {filename: self.read_file(filename) for filename in filenames_to_compare}
        files_to_compare = {filename: file for filename, file in files_to_compare.items() if file}

        return self.compare(files_to_compare)

    def compare(self, files_to_compare: dict):
        my_logger.info("Comparing files")
        files_pair = [(pair[0], pair[1]) for pair in product(files_to_compare.keys(), repeat=2) if pair[0] < pair[1]]
        results = {}

        for filename_1, filename_2 in files_pair:
            file_1 = files_to_compare[filename_1]
            file_2 = files_to_compare[filename_2]
            if self.parse_python:
                alphabet = {word: chr(40 + index) for index, word in enumerate(set(file_1).union(set(file_2)))}
            else:
                alphabet = None

            result = [self.predict(file_1, file_2, predicting_functions[metric], alphabet) for metric in self.metrics]
            results[(filename_1, filename_2)] = result

        return results

    def preprocessing(self, filename):
        """
        filename: filename not file itself

        use node-visitors for getting a list from ast tree
        first sort all nodes, so they are matched by their sizes
        """
        my_logger.info("Code preprocessing")
        code = self.read_file(filename)

        if not code:
            return None

        try:
            return self.preprocessing_code(code)
        except SyntaxError as e:
            my_logger.error("Syntax error has occurred")
            print_color(f'{e} in file {filename}', color='red')
            sys.exit(1)

    @staticmethod
    def preprocessing_code(code):
        node_visitor = Visitor()
        node_sorter = NodeSorting()
        tree = ast.parse(code)

        node_sorter.run(tree)
        node_visitor.generic_visit(tree)

        return node_visitor.data

    @staticmethod
    def predict(code1, code2, metric, alphabet):
        try:
            if alphabet:
                code1 = ''.join(alphabet[el] for el in code1)
                code2 = ''.join(alphabet[el] for el in code2)
            return metric(code1, code2)
        except SyntaxError:
            my_logger.error("Syntax error has been occurred")
            return 0
