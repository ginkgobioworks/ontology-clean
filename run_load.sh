#!/bin/bash
set -eu -o pipefail

ORIG=`pwd`
cd tools/SciGraph/SciGraph-core
mvn exec:java -Dexec.mainClass="io.scigraph.owlapi.loader.BatchOwlLoader" -Dexec.args="-c $ORIG/config/load.yaml"
