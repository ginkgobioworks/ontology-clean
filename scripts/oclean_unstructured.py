#!/usr/bin/env python
"""Mapping unstructured keys into ontologies with grouped entity, attribute, values.
"""
import sys

import oclean.group

def main(in_file):
    params = {"cleaner": key_clean_common, "kmer": 5,
              "norm_map": {"raw": "raw", "ideal": "ideal"}}
    with open(in_file) as in_handle:
        in_keys = [l.strip() for l in in_handle]
    clusters = oclean.group.cluster_keys(in_keys, params)
    for cid in sorted(clusters.keys()):
        print("-", clusters[cid])

def key_clean_common(k):
    """Provide transformations for common conventions used inconsistently in key names.
    """
    # Avoid underscore attached raw specifications
    k = k.replace("_raw", " raw")
    # Separate colon separated items like OD600:600
    k = k.replace(":", " ")
    return k


if __name__ == "__main__":
    main(*sys.argv[1:])
