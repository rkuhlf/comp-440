from collections import Counter

import helpers

import random

from collections import Counter

def centroid(strings):
    L = len(strings[0])
    result = []
    for i in range(L):
        counts = Counter(s[i] for s in strings)
        result.append(counts.most_common(1)[0][0])
    return "".join(result)

def kmeans_strings(data, k, max_iters=100):
    # Initialize centroids randomly from data
    centroids = random.sample(data, k)

    for _ in range(max_iters):
        clusters = [[] for _ in range(k)]

        # Assignment step
        for s in data:
            distances = [helpers.gene_diff(s, c) for c in centroids]
            idx = distances.index(min(distances))
            clusters[idx].append(s)

        # Update step
        new_centroids = []
        for cluster in clusters:
            if cluster:
                new_centroids.append(centroid(cluster))
            else:
                # Empty cluster → reinitialize
                new_centroids.append(random.choice(data))

        # Convergence check
        if new_centroids == centroids:
            break
        centroids = new_centroids

    return centroids, clusters



if __name__ == "__main__":
    data = [
        "00120000001022200303321321321321321321131131131131",
        "00100000111022200003111111111111122111330330331300",
        "00020000000002200300321321321121321321131133131101",
        "03100000001120203033311121121111212122130331030131",
        "00020000020002200300321321321121321121131133120131",
        "00020000001122220030323321323122123321303100330313",
        "01000000111102203333333233333223223233113103203113",
        "03130000030000003313311121121122222122131130131131",
        "00000010113102200000321333333223223333310313313311",
        "00020000000002200000321321321121321321131133131121",
        "01300000101120200033133323223322232333313333010310",
        "01000001113122200330322233133223223233130100230313",
        "00100000111120203003111111111111121111331330331300",
        "00020000001002200000321321321121321321131133121121",
        "00300000000122203330323333333333233233110103110110",
        "10020000111122203333233212112222111212310110231311",
        "10000003111122320133333333233222232332301133010310",
        "03000000111100203333122211111211221221301131300300",
        "00020000001022220300321321123121321121133300213101",
        "01300000010102003330133323323322122323313313113310",
        "00020000011122200000123323123123123123303313303311",
        "33320000130122203333232232232232232222130130111130",
        "03100000030000003330311121121121322122131131101130",
    ]
    centroids, clusters = kmeans_strings(data, 4)

    for c, cluster in zip(centroids, clusters):
        mean_diff = sum([helpers.gene_diff(c, d) for d in cluster]) / len(cluster)
        print(f"{c}, {mean_diff:.0f}")
        # print(cluster)
