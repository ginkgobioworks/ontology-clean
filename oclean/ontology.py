"""Map terms to ontology groupings using pre-defined regular expression based rules.
"""
import urllib.parse
import re

import edn_format
import requests

def _read_rules(rule_file):
    def _clean_key(k):
        return k.name if isinstance(k, edn_format.Keyword) else k
    def _clean_dict(xs):
        if isinstance(xs, (dict, edn_format.immutable_dict.ImmutableDict)):
            return {_clean_key(k): _clean_dict(v) for k, v in xs.items()}
        if isinstance(xs, (list, tuple)):
            return [_clean_dict(x) for x in xs]
        else:
            return xs
    with open(rule_file) as in_handle:
        return _clean_dict(edn_format.loads(in_handle.read()))["rules"]

def _find_rule_matches(w, rules, scigraph):
    """Find any rules matching from a word.
    """
    avs = []
    for r in rules:
        m = re.search(r["pat"], w)
        if m:
            if "custom" in r:
                term = {"term": r["custom"]}
            elif "search" in r:
                term = get_term_by_search(r["search"], scigraph)
            else:
                term = get_term_by_id(r["ontology"], scigraph)
            avs.append((term, "VAL"))
            for k, v in m.groupdict().items():
                avs.append((_find_rule_matches(k, rules, scigraph)[0][0], v))
    return avs

def _remove_dups(avs):
    seen = set([])
    out = []
    for key, val in avs:
        cur = (key["term"], val)
        if cur not in seen:
            seen.append(cur)
            out.append((key, val))
    return out

def rule_mapper(rule_file, params):
    """Provide function to map terms to ontologies and values given input rules.
    """
    rules = _read_rules(rule_file)

    def _from_token(token):
        avs = []
        for w in token.words:
            avs.extend(_find_rule_matches(w, rules, params["scigraph"]))
        for attr in ["units", "normalization"]:
            xs = getattr(token, attr)
            if xs:
                cura = _find_rule_matches(attr, rules, params["scigraph"])[0][0]
                avs += [(cura, x) for x in xs]
        return avs

    return _from_token

# ## SciGraph support

def get_term_by_search(search, base_url):
    """Retrieve an ontology term by search.
    """
    search_id = urllib.parse.quote('"%s"' % (search), safe="")
    url = f"{base_url}/vocabulary/search/{search_id}"
    for term in requests.get(url).json():
        if term["labels"][0].find(search) >= 0:
            return {"term": term["labels"][0], "iri": term["iri"],
                    "definition": term["definitions"][0]}

def get_term_by_id(iri, base_url):
    """Retrieve ontology term details by an ontology identifier.
    """
    id_prefixes = {"obi": "http://purl.obolibrary.org/obo/",
                   "bao": "http://www.bioassayontology.org/bao#"}
    search_id = urllib.parse.quote("%s%s" % (id_prefixes[iri.split("_")[0].lower()], iri), safe="")
    url = f"{base_url}/vocabulary/id/{search_id}"
    term = requests.get(url).json()
    return {"term": term["labels"][0], "iri": term["iri"],
            "definition": term["definitions"][0]}
