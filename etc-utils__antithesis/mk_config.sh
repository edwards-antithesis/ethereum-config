#!/usr/bin/env sh

if [[ $# -ne 2 ]]; then 
  echo "$0 config-file image-tag"
  exit -1
fi

config=$1
tag=$2

make clean
make base
podman run -v ./shared-data/:/data/ -v .:/source/ etc-builder:latest python3 /source/create_scenario.py --config /source/configs/$config --docker --bootstrap-mode
if [[ $? -eq 0 ]]; then
  podman build --build-arg config=$config --format docker -f config.dockerfile -t "us-central1-docker.pkg.dev/molten-verve-216720/ethereum-repository/$tag"
else
  echo "WARNING: problems with generating the config -- skipping building config image"
fi
