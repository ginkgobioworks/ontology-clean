#!/bin/env python
"""Map rules into a set of finalized ontologies with names and documentation.
"""
import collections
import os
import shelve
import sys

from oclean import ontology

def main(rules):
    params = {"lookup_cache": os.path.join("cache", "ontology_lookups.db"),
              "scigraph": "http://localhost:9000/scigraph"}
    with shelve.open(params["lookup_cache"]) as lookup_db:
        params["lookup_db"] = lookup_db
        out_rules = ontology.expand_rules(rules, params)
    out_file = "%s-hodur.edn" % os.path.splitext(rules)[0]
    with open(out_file, "w") as out_handle:
        out_handle.write(rules_to_hodur(out_rules))

def rules_to_hodur(schema):
    """Convert ontology rule representations to Hodur syntax.
    """
    hodur_types = {"string": "String", "float": "Float", "integer": "Integer", "long": "Integer"}
    out = []
    namespaces = collections.defaultdict(list)
    for o in schema:
        namespaces[o.get("ns")].append(o)
    for namespace, attributes in namespaces.items():
        if namespace:
            namespace = "".join(namespace.replace("-", " ").title().split())
        else:
            namespace = ""
        out.append("%s [" % namespace)
        for a in attributes:
            name = a["term"]
            if a["doc"] != name:
                doc = ' :doc "%s"' % a["doc"]
            else:
                doc = ""
            out.append("^{:type %s%s} %s" % (hodur_types[a.get("value_type") or "string"], doc, name))
        out.append("]")
    return "\n".join(out) + "\n"

if __name__ == "__main__":
    main(*sys.argv[1:])
