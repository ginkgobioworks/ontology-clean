#!/bin/bash
set -eu -o pipefail

mkdir -p tools
cd tools
#git clone https://github.com/SciGraph/SciGraph
cd SciGraph
#mvn -DskipTests -DskipITs install

cd ..
wget https://github.com/OpenRefine/OpenRefine/releases/download/3.2-beta/openrefine-linux-3.2-beta.tar.gz
tar -xzvpf openrefine*.tar.gz
rm openrefine*.tar.gz
mv openrefine-* openrefine
