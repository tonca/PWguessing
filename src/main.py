import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import csv
import pandas as pd
import string

from sklearn.cluster import dbscan
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import AffinityPropagation
from leven import levenshtein


print("helo")

def _flatten_string(word):
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

def lev_metric_flat(x,y):
    i, j = int(x[0]), int(y[0])     # extract indices

    flat1 = _flatten_string(data[i])
    flat2 = _flatten_string(data[j])

    return levenshtein(flat1, flat2)


def lev_metric(x, y):
    i, j = int(x[0]), int(y[0])     # extract indices

    return levenshtein(str(data[i]), str(data[j]))

def lev_metric_avg(x,y):
    return lev_metric(x,y) + lev_metric_flat(x,y)

def read_list() :
    fname = "used";
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    return content
            


if __name__ == "__main__":

    list_used = read_list()

    df = pd.read_csv(list_used[0], delimiter=':', names=['user','password'])

    print(df.describe())

    data = df['password'][:]

    set_size = 500

    X = np.random.choice(len(data), set_size).reshape(-1, 1)

    n_clusters = 10

    lev_similarity = np.array([[lev_metric_avg(w1,w2) for w1 in X] for w2 in X])

    # model = dbscan(X, metric=lev_metric, eps=5, min_samples=2)

    model = AgglomerativeClustering(n_clusters=n_clusters, linkage='complete', affinity='precomputed')

    # model = AffinityPropagation(affinity='precomputed', damping=0.9)

    model.fit(lev_similarity)

    print model.labels_


    for cluster_id in range(0, n_clusters) : 
        print "--------------------------------------"
        cluster_elems = np.where(model.labels_ == cluster_id)
        cluster = X[cluster_elems].reshape(-1)
        for el in data[cluster] : 
            print "%s : %s" % (el, _flatten_string(el))

    # for cluster_id in np.unique(model.labels_):
    #     print "--------------------------------------"
    #     exemplar = X[model.labels_[cluster_id]]
    #     cluster = np.unique(X[np.nonzero(model.labels_==cluster_id)])
    #     cluster_str = ", ".join(data[cluster])
    #     print(" - *%s:*\n%s" % (data[exemplar], cluster_str))
