import jellyfish
import numpy as np
import string
from itertools import groupby


def mask_string(word):
    word = str(word)

    out = ""
    
    for c in word:
        next = 'x'
        if c in string.ascii_lowercase:
            next = 'l'
        if c in string.ascii_uppercase:
            next = 'u'
        if c in string.digits:
            next = 'd'
        if c in string.punctuation:
            next = 'p'
        out += next

    return out

def flatten_string(word):
    word = mask_string(word)

    return ''.join([ k[0] for k in groupby(word) ])


class distance_measurer :

    def __init__(self, data):
        self.data = data

    ## MIXED STRATEGY

    def mixed_metric(self, x, y):

        return self.lev_metric_flat(x,y) + self.lev_metric_mask(x,y) + self.jac_metric(x,y)


    ## DAMERAU LEVENSHTEIN DISTANCE (edit distance improved)

    def lev_metric_flat(self, x, y):
        i, j = int(x[0]), int(y[0])     # extract indices

        flat1 = flatten_string(self.data[i])
        flat2 = flatten_string(self.data[j])

        return jellyfish.damerau_levenshtein_distance(flat1, flat2)

    def lev_metric_mask(self, x, y):
        i, j = int(x[0]), int(y[0])     # extract indices

        mask1 = mask_string(self.data[i])
        mask2 = mask_string(self.data[j])

        return jellyfish.damerau_levenshtein_distance(mask1, mask2)

    def lev_metric(self, x, y):
        i, j = int(x[0]), int(y[0])     # extract indices

        return jellyfish.damerau_levenshtein_distance(str(self.data[i]), str(self.data[j]))

    def lev_metric_avg(self, x, y):
        return lev_metric(x,y) + lev_metric_flat(x,y)


    ## JACCARD DISTANCE

    def _jaccard(self, a, b):
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    def jac_metric(self, x, y):
        i, j = int(x[0]), int(y[0])     # extract indices

        set1 = set(str(self.data[i]))
        set2 = set(str(self.data[j]))

        return self._jaccard(set1,set2)