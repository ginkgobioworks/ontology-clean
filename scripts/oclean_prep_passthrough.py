#!/usr/bin/env python
"""Prepare pass through values into ontology rules with grouping by namespaces.
"""
import csv
import os
import sys

import oclean.ontology

def main(in_file):
    with open(in_file) as in_handle:
        reader = csv.reader(in_handle)
        header = next(reader)
        rules = []
        for parts in reader:
            row = dict(zip(header, parts))
            if include_term(row):
                rule = convert_to_custom_rule(row)
                rules.append(rule)
    rules.sort(key=lambda x: (x["ns"], x["pat"].lower()))
    with open("%s-custom.edn" % os.path.splitext(in_file)[0], "w") as out_handle:
        for rule in rules:
            out_handle.write('  {:pat "%s" :type "%s" :ns "%s"}\n' %
                             (rule["pat"], rule["value_type"], rule["ns"]))

def include_term(row):
    if row["origkey"].startswith("ex") and row["origkey"].find("em") > 0:
        return False
    elif row["origkey"].startswith("OD"):
        return False
    elif row["origkey"] in ["Timepoint", "units"]:
        return False
    else:
        return True

def convert_to_custom_rule(row):
    rule = {}
    rule["pat"] = row["origkey"]
    rule = oclean.ontology.add_value_type(rule, {}, [row["value"]])
    if row["namespace"] == "ferment-timepoint":
        if row["chemical"].lower() in ["true"]:
            ns = "chemical-measures/entity-measure"
        else:
            ns = "reactor-measures/entity-measure"
    else:
        ns = row["namespace"]
    rule["ns"] = ns
    return rule

if __name__ == "__main__":
    main(*sys.argv[1:])
