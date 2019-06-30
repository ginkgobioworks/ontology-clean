#!/bin/bash
set -eu -o pipefail

mkdir -p store/inputs
mkdir -p store/graph
cd store/inputs
[ -f "so.owl" ] || wget https://github.com/The-Sequence-Ontology/SO-Ontologies/raw/master/so.owl
[ -f "bao_complete.owl" ] || wget http://www.bioassayontology.org/bao/bao_complete.owl
[ -f "obi.owl" ] || wget http://purl.obolibrary.org/obo/obi.owl
[ -f "chebi.owl" ] || wget -O - http://purl.obolibrary.org/obo/chebi.owl.gz | gunzip -c > chebi.owl
[ -f "ncit.owl" ] || wget http://purl.obolibrary.org/obo/ncit.owl
[ -f "sbo.owl" ] || wget http://purl.obolibrary.org/obo/sbo.owl
[ -f "rhea-biopax.owl" ] || wget -O - ftp://ftp.expasy.org/databases/rhea/biopax/rhea-biopax.owl.gz | gunzip -c > rhea-biopax.owl
[-f "stato.owl"] || wget http://purl.obolibrary.org/obo/stato.owl
