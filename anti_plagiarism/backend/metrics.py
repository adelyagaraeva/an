import jellyfish


# requirement for new metrics: it takes two string and return an int or a float:
#
# def metrics(str1: str, str2: str) -> int or float:
#     pass


def lev_normalized(code1, code2):
    """
    levenshtein distance divided by maximum of sizes of texts in order to normalize it
    """
    return 1 - jellyfish.levenshtein_distance(code1, code2) / max(len(code1), len(code2))


def dam_lev_normalized(code1, code2):
    """
    damerau-levenshtein distance divided by maximum of sizes of texts in order to normalize it
    """
    return 1 - jellyfish.damerau_levenshtein_distance(code1, code2) / max(len(code1), len(code2))


# You must add new metric here
predicting_functions = {'lev': jellyfish.levenshtein_distance,
                        'dam-lev': jellyfish.damerau_levenshtein_distance,
                        'jaro': jellyfish.jaro_similarity,
                        'lev-norm': lev_normalized,
                        'dam-lev-norm': dam_lev_normalized,
                        'jaro-win': jellyfish.jaro_winkler_similarity
                        }

# You must add new metric here if it is increasing from large commonalities of two texts
increasing_from_plagiarism = ['jaro', 'lev-norm', 'dam-lev-norm', 'jaro-win']
