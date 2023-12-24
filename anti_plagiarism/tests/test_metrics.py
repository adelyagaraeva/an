import pytest

from backend.metrics import *

levenshtein_distance = predicting_functions['lev']
damerau_levenshtein_distance = predicting_functions['dam-lev']


def test_levenshtein_same_strings():
    assert levenshtein_distance("kitten", "kitten") == 0


def test_levenshtein_one_empty_string():
    assert levenshtein_distance("", "kitten") == 6
    assert levenshtein_distance("kitten", "") == 6


def test_levenshtein_insertions():
    assert levenshtein_distance("kitten", "kittens") == 1
    assert levenshtein_distance("sitting", "sittin") == 1


def test_levenshtein_deletions():
    assert levenshtein_distance("kitten", "kiten") == 1
    assert levenshtein_distance("sitting", "sittin") == 1


def test_levenshtein_substitutions():
    assert levenshtein_distance("kitten", "kittin") == 1
    assert levenshtein_distance("sitting", "sittang") == 1


def test_levenshtein_complex_case():
    assert levenshtein_distance("kitten", "sitting") == 3


def test_damerau_levenshtein_same_strings():
    assert damerau_levenshtein_distance("kitten", "kitten") == 0


def test_damerau_levenshtein_one_empty_string():
    assert damerau_levenshtein_distance("", "kitten") == 6
    assert damerau_levenshtein_distance("kitten", "") == 6


def test_damerau_levenshtein_insertions():
    assert damerau_levenshtein_distance("kitten", "kittens") == 1
    assert damerau_levenshtein_distance("sitting", "sittin") == 1


def test_damerau_levenshtein_deletions():
    assert damerau_levenshtein_distance("kitten", "kiten") == 1
    assert damerau_levenshtein_distance("sitting", "sittin") == 1


def test_damerau_levenshtein_substitutions():
    assert damerau_levenshtein_distance("kitten", "kittin") == 1
    assert damerau_levenshtein_distance("sitting", "sittang") == 1


def test_damerau_levenshtein_transpositions():
    assert damerau_levenshtein_distance("kitten", "kittne") == 1
    assert damerau_levenshtein_distance("sitting", "sittign") == 1


def test_damerau_levenshtein_complex_case():
    assert damerau_levenshtein_distance("kitten", "sitting") == 3


if __name__ == "__main__":
    pytest.main()
