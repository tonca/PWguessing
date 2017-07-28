import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import KMeans
from sklearn.cluster import dbscan
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import AffinityPropagation

import distance_functions as dist
import precompute_distances

print("helo")

def read_list() :
    fname = "used";
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    return content

def compute_mat(X,measurer):
    return pairwise_distances(X, metric=measurer.mixed_metric)


if __name__ == "__main__":

    list_used = read_list()

    df = pd.read_csv(list_used[0], delimiter=':', names=['user','password'])

    print(df.describe())

    data = df['password'][:]

    set_size = 500

    X = np.random.choice(len(data), set_size).reshape(-1, 1)

    n_clusters = 10

    measurer = dist.distance_measurer(data)

    similarity_mat = compute_mat(X,measurer)

    model = AgglomerativeClustering(n_clusters=n_clusters, linkage='complete', affinity='precomputed')

    model.fit(similarity_mat)

    print model.labels_


    for cluster_id in range(0, n_clusters) : 
        print "--------------------------------------"
        cluster_elems = np.where(model.labels_ == cluster_id)
        cluster = X[cluster_elems].reshape(-1)
        for el in data[cluster] : 
            print "%s : %s : %s" % (el, dist.mask_string(el), dist.flatten_string(el))