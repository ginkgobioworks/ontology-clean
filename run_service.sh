#!/bin/bash
set -eu -o pipefail

ORIG=`pwd`
cd tools/SciGraph/SciGraph-services
mvn exec:java -Dexec.mainClass="io.scigraph.services.MainApplication" -Dexec.args="server $ORIG/config/service.yaml"
