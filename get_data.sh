#!/bin/bash
set -eu -o pipefail

mkdir -p store/inputs
mkdir -p store/graph
cd store/inputs
wget https://github.com/The-Sequence-Ontology/SO-Ontologies/raw/master/so.owl
wget http://www.bioassayontology.org/bao/bao_complete.owl
