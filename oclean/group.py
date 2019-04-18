"""Group
"""
import collections
from functools import reduce
import operator
import pprint
import re

import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.metrics import distance
import sklearn.cluster
import pint


def cluster_keys(in_kvs, params):
    """Take a set of input key/value pairs and normalize and cluster into groups.
    """
    tokenizer = RegexpTokenizer(r'[\w/=]+')
    tokens = []
    ivals = {}
    # Provide index mapping keys to values for retrieval
    for i, (in_key, in_val) in enumerate(in_kvs):
        ivals[i] = in_val
        tokens.append((i, tokenizer.tokenize(params["cleaner"](in_key.strip().lower()))))
    tokens = [_add_normalization(i, add_units(t), params["norm_map"]) for (i, t) in tokens]
    assert len(tokens) == len(in_kvs)
    cluster_indexes = distance_clustering([x.words for x in tokens], params["kmer"])
    # words = [["_".join(x.words)] for x in tokens]
    # word2vec_kmeans(words)
    clusters = collections.defaultdict(list)
    # Re-associated values after key organization
    for i, t in enumerate(tokens):
        clusters[cluster_indexes[i]].append((t, ivals[t.valindex]))
    return clusters

def _word_to_kmers(w, kmer_size):
    """Find useful kmer sub-words within the top level.
    """
    # Full word plus subsets
    kmers = []
    if (len(w) <= kmer_size):
        kmers.append(w)
    else:
        for i in range(len(w) - kmer_size):
            kmers.append(w[i:i + kmer_size])
    # Any non single digit integers (wavelengths and friends)
    for digits in re.findall(r"\d\d+", w):
        kmers.append(digits)
    return kmers

def term_distance(ws1, ws2, kmer_size):
    """Calculate term distances, using words from 2 different terms.

    Uses Levenshtein distance as basis but handles special cases where
    subsets of kmers match identically.
    """
    max_len = max([len(w) for w in ws1] + [len(w) for w in ws2])
    w1_mers = reduce(operator.add, [_word_to_kmers(w, kmer_size) for w in ws1])
    w2_mers = reduce(operator.add, [_word_to_kmers(w, kmer_size) for w in ws2])
    distances = []
    for w1 in w1_mers:
        for w2 in w2_mers:
            if w1.find(w2) >= 0 or w2.find(w1) >= 0:
                distances.append(0)
            else:
                distances.append(distance.edit_distance(w1, w2) / max_len)
    return min(distances) if min(distances) == 0 else 0.05

def _split_cluster(words, kmer_size):
    """Potentially split up a cluster based on more precise matches.

    Automated clustering methods can be overly aggressive in clustering
    unrelated terms, and this adds additional stringency.
    """
    out = [[words[0]]]
    for w in words[1:]:
        added = False
        for i, wout in enumerate(out):
            if all([term_distance(w, w2, kmer_size) == 0 for w2 in wout]):
                out[i].append(w)
                added = True
                break
        if not added:
            out.append([w])
    return out

def distance_clustering(words, kmer_size):
    """Cluster words based on edit distance.
       2 pass approach:
          - Broad clustering of things with matching larger k-mers and digits
          - Split clusters with in groups without larger k-mer matches.
    """
    word_to_origi = collections.defaultdict(list)
    for i, w in enumerate(words):
        word_to_origi[tuple(w)].append(i)
    words = np.asarray(words)
    similarity = -1 * np.array([[term_distance(w1, w2, kmer_size) for w1 in words] for w2 in words])
    affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(similarity)
    word_to_cluster = {}
    cluster_i = 0
    for cluster_id in np.unique(affprop.labels_):
        orig_cluster = np.unique(words[np.nonzero(affprop.labels_ == cluster_id)])
        for cluster in _split_cluster(orig_cluster, kmer_size):
            for w in cluster:
                for origi in word_to_origi[tuple(w)]:
                    word_to_cluster[origi] = cluster_i
            cluster_i += 1
    return word_to_cluster

def _add_normalization(valindex, token, norm_map):
    """Flag words used to describe normalization inputs.
    """
    AnnToken = collections.namedtuple("AnnToken", "words,units,normalization,valindex")
    cur_words = []
    cur_norms = []
    for w in token.words:
        if w in norm_map:
            cur_norms.append(w)
        else:
            cur_words.append(w)
    return AnnToken(cur_words, token.units, cur_norms,valindex)

def add_units(tokens):
    """Separate specifications into descriptions of process and units.

    Handles both flexible units via pint and also more standardized
    things used (raw).
    """
    WordUnits = collections.namedtuple("WordUnits", "words,units")
    ureg = pint.UnitRegistry()
    words = []
    units = []
    for w in tokens:
        try:
            cur = ureg(w)
        except pint.errors.UndefinedUnitError:
            cur = None
        if cur and hasattr(cur, "units"):
            units.append(str(cur.units))
        else:
            words.append(w)
    return WordUnits(words, units)

def word_modeling(tokens):
    from gensim.corpora import Dictionary
    from gensim.models import phrases, LdaModel, Word2Vec

    bigram = phrases.Phraser(phrases.Phrases(tokens, min_count=2))
    for i, ts in enumerate(tokens):
        for btoken in bigram[ts]:
            if '_' in btoken and btoken not in tokens[i]:
                tokens[i].append(btoken)

    token_dict = Dictionary(tokens)
    corpus = [token_dict.doc2bow(t) for t in tokens]

    _ = token_dict[0]
    model = LdaModel(corpus=corpus, id2word=token_dict.id2token, chunksize=len(tokens), alpha="auto",
                     eta="auto", iterations=400, num_topics=20, passes=20, eval_every=None)
    pprint.pprint(model.top_topics(corpus))

def word2vec_kmeans(words):
    """Word2vec encoding and k-means clustering, not especially good on terms.
    """
    from gensim.models import phrases, Word2Vec
    import nltk.cluster

    num_clusters = 20
    method = "nltk"
    # bigram = phrases.Phraser(phrases.Phrases(words, min_count=1))
    model = Word2Vec(words, min_count=1)

    X = model.wv

    if method == "sklearn":
        clusterer = sklearn.cluster.KMeans(n_clusters=10, n_init=50, random_state=42)
        assigned_clusters = clusterer.fit_predict(X.vectors)
    else:
        assert method == "nltk"
        clusterer = nltk.cluster.KMeansClusterer(num_clusters,
                                                  distance=nltk.cluster.util.cosine_distance, repeats=25)
        clusterer = nltk.cluster.GAAClusterer(num_clusters)
        assigned_clusters = clusterer.cluster(X.vectors, assign_clusters=True)

    wclusters = collections.defaultdict(list)
    for i, word in enumerate(list(X.index2word)):
        wclusters[assigned_clusters[i]].append(word)
    for c in sorted(list(wclusters.keys())):
        print(c, wclusters[c])

