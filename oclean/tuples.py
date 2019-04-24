"""Map input measurements into tuples of entity -- attribute -- value.

Flattens key values with embedded information on units and other
external data, along mapping to ontologies.

Uses externally written business rules for how to map word names into
ontologies.
"""
import collections

import edn_format
from edn_format import Keyword as K

def flatten_to_ontology(token_vals, mapper):
    """Given a token, flatten into a series of key/value pairs and an ontology.
    """
    ns_groups = collections.defaultdict(list)
    for token, val in token_vals:
        for okey, val in mapper(token, val):
            ns = okey["term"].split("/")[0]
            ns_groups[ns].append((okey, val))
    for ns, cur_o in ns_groups.items():
        yield _ontology_to_edn(cur_o)

def _ontology_to_edn(cur_o):
    """Map an ontology specification to datomic schemas and inputs.
    """
    schema = []
    vals = []
    for okey, val in cur_o:
        cur_id = K(okey["term"])
        schema.append({"ident": cur_id,
                       "valueType": K("db.type/%s" % okey["value_type"]),
                       "cardinality": K("db.cardinality/one"),
                       "doc": okey.get("doc", "")})
        vals.append((cur_id, val))
    return (edn_format.dumps(schema, keyword_keys=True, sort_keys=True),
            edn_format.dumps(vals, keyword_keys=True, sort_keys=True))
