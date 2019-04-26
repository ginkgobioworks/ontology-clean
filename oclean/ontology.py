"""Map terms to ontology groupings using pre-defined regular expression based rules.
"""
import pprint
import urllib.parse
import re

import edn_format
import requests

def edn_loads_clean(x):
    def _clean_key(k):
        return k.name if isinstance(k, edn_format.Keyword) else k

    def _clean_dict(xs):
        if isinstance(xs, (dict, edn_format.immutable_dict.ImmutableDict)):
            return {_clean_key(k): _clean_dict(v) for k, v in xs.items()}
        elif isinstance(xs, (list, tuple, edn_format.immutable_list.ImmutableList)):
            return [_clean_dict(x) for x in xs]
        else:
            return _clean_key(xs)
    return _clean_dict(edn_format.loads(x))

def _read_rules(rule_file):
    with open(rule_file) as in_handle:
        return edn_loads_clean(in_handle.read())["rules"]

def _find_rule_matches(w, rules, scigraph, vals, cur_ns=None):
    """Find any rules matching from a word.
    """
    avs = []
    for r in rules:
        m = re.search(r["pat"], w)
        if m:
            if "custom" in r:
                term = {"term": r["custom"], "doc": r.get("doc") or r["custom"]}
            elif "search" in r:
                term = get_term_by_search(r["search"], scigraph)
            else:
                term = get_term_by_id(r["ontology"], scigraph)
            term = _add_value_type(term, r, vals)
            for val in vals:
                avs.append((term, _convert_val(val, term["value_type"])))
            if cur_ns or "ns" in r:
                avs = [(_add_namespace(a, cur_ns or r["ns"]), v) for a, v in avs]
            if not cur_ns:
                cur_ns = _get_cur_namespace(avs)
                avs = [(_add_namespace(a, cur_ns), v) for a, v in avs]
            for k, v in m.groupdict().items():
                avs.extend(_find_rule_matches(k, rules, scigraph, [v], cur_ns))
    return avs

def _get_cur_namespace(avs):
    """Get a current namespace, either existing or default.
    """
    cur_term = avs[0][0]["term"].split("/")
    if len(cur_term) == 1:
        return avs[0][0]["term"]
    else:
        assert len(cur_term) == 2, pprint.pformat(avs)
        return cur_term[0]

def _add_namespace(attr, ns):
    """Add a namespace to a attribute, if not already namespaced.

    Allows grouping of terms by name.
    """
    cur_term = attr["term"].split("/")
    if len(cur_term) == 1:
        attr["term"] = "%s/%s" % (ns, attr["term"])
    else:
        assert len(cur_term) == 2, (attr)
    return attr

def _convert_val(val, value_type):
    if val in [None]:
        return val
    if value_type == "long":
        return int(val)
    elif value_type == "float":
        return float(val)
    else:
        return val

def _add_value_type(term, rule, vals):
    """Add value type from definition, or guessing based on value.
    """
    if "type" in rule:
        val_type = rule["type"]
    else:
        for val in vals:
            if val is None:
                val_type = "string"
            else:
                try:
                    int(val)
                    val_type = "long"
                    break
                except ValueError:
                    try:
                        float(val)
                        val_type = "float"
                        break
                    except ValueError:
                        val_type = "string"
    term["value_type"] = val_type
    return term

def _remove_dups(avs):
    seen = set([])
    out = []
    for key, val in avs:
        cur = (key["term"], val)
        if cur not in seen:
            seen.append(cur)
            out.append((key, val))
    return out

def _clean_attribute(attr):
    attr["term"] = attr["term"].replace(" ", "-")
    return attr

def rule_mapper(rule_file, params):
    """Provide function to map terms to ontologies and values given input rules.
    """
    rules = _read_rules(rule_file)

    def _from_token(token, val):
        avs = []
        for w in token.words:
            avs.extend(_find_rule_matches(w, rules, params["scigraph"], [val]))
        if len(avs) == 0:
            avs.extend(_find_rule_matches(" ".join([w for w in token.words]),
                                          rules, params["scigraph"], [val]))
        if len(avs) == 0:
            raise NotImplementedError("Missing ontology mapping for:\n%s" % str(token))
        for attr in ["units", "normalization"]:
            xs = getattr(token, attr)
            if xs:
                avs.extend(_find_rule_matches(attr, rules, params["scigraph"], xs,
                                              _get_cur_namespace(avs)))
        avs = [(_clean_attribute(a), v) for a, v in avs]
        return avs

    return _from_token

# ## SciGraph support

def get_term_by_search(search, base_url):
    """Retrieve an ontology term by search.
    """
    search_id = urllib.parse.quote('"%s"' % (search), safe="")
    url = f"{base_url}/vocabulary/search/{search_id}"
    results = requests.get(url).json()
    if not (isinstance(results, dict) and results.get("code") == 404):
        for term in results:
            if term["labels"][0].find(search) >= 0:
                return {"term": term["labels"][0], "iri": term["iri"],
                        "doc": _get_doc(term)}
    raise ValueError("Did not find ontology term for search '%s'\n%s" %
                     (search, pprint.pformat(results)))

def _get_doc(term):
    out = term["iri"]
    if term.get("definitions"):
        out += ": %s" % (term["definitions"][0])
    return out

def get_term_by_id(iri, base_url):
    """Retrieve ontology term details by an ontology identifier.
    """
    id_prefixes = {"obi": "http://purl.obolibrary.org/obo/",
                   "bao": "http://www.bioassayontology.org/bao#"}
    search_id = urllib.parse.quote("%s%s" % (id_prefixes[iri.split("_")[0].lower()], iri), safe="")
    url = f"{base_url}/vocabulary/id/{search_id}"
    term = requests.get(url).json()
    return {"term": term["labels"][0], "iri": term["iri"],
            "doc": _get_doc(term)}
