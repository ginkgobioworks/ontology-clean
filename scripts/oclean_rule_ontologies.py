#!/bin/env python
"""Map rules into a set of finalized ontologies with names and documentation.
"""
import os
import shelve
import sys

from oclean import ontology

def main(rules):
    params = {"lookup_cache": os.path.join("cache", "ontology_lookups.db"),
              "scigraph": "http://localhost:9000/scigraph"}
    with shelve.open(params["lookup_cache"]) as lookup_db:
        params["lookup_db"] = lookup_db
        ontology.expand_rules(rules, params)


if __name__ == "__main__":
    main(*sys.argv[1:])
