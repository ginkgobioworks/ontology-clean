#!/usr/bin/env python
"""Mapping unstructured keys into ontologies with grouped entity, attribute, values.
"""
import os
import pprint
import shelve
import sys

import oclean.group
import oclean.ontology
import oclean.tuples

def main(in_file, rules):
    params = {"cleaner": key_clean_common, "kmer": 5,
               "norm_map": {"raw": "raw"},
               "lookup_cache": os.path.join("cache", "ontology_lookups.db"),
               "scigraph": "http://localhost:9000/scigraph"}
    # Use temporary value for testing with sets of input keys
    default_key = None
    with open(in_file) as in_handle:
        in_kvs = [(l.strip(), default_key) for l in in_handle]
    with shelve.open(params["lookup_cache"]) as lookup_db:
        params["lookup_db"] = lookup_db
        clusters = oclean.group.cluster_keys(in_kvs, params)
        mapper = oclean.ontology.rule_mapper(rules, params)
        token_vals = []
        for cid in sorted(clusters.keys()):
            for token, val in clusters[cid]:
                token_vals.append((token, val))
        for o_edn, kv_edn in oclean.tuples.flatten_to_ontology(token_vals, mapper):
            pprint.pprint(o_edn)
            pprint.pprint(kv_edn)

def key_clean_common(k):
    """Provide transformations for common conventions used inconsistently in key names.
    """
    # Avoid underscore attached raw specifications
    k = k.replace("_raw", " raw")
    # Separate colon separated items like OD600:600
    k = k.replace(":", " ")
    k = k.replace("-", " ")
    return k

if __name__ == "__main__":
    main(*sys.argv[1:])
