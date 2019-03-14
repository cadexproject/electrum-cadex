#!/bin/bash
set -ev

if [[ -z $TRAVIS_TAG ]]; then
  echo TRAVIS_TAG unset, exiting
  exit 1
fi

BUILD_REPO_URL=https://github.com/cadex/electrum-cadex.git

cd build

git clone --branch $TRAVIS_TAG $BUILD_REPO_URL electrum-cadex

docker run --rm \
    -v $(pwd):/opt \
    -w /opt/electrum-cadex \
    -t zebralucky/electrum-cadex-winebuild:Linux /opt/build_linux.sh

sudo find . -name '*.po' -delete
sudo find . -name '*.pot' -delete

sudo chown -R 1000 electrum-cadex

docker run --rm \
    -v $(pwd)/electrum-cadex:/home/buildozer/build \
    -t zebralucky/electrum-cadex-winebuild:KivyPy36 bash -c \
    'export LANG=en_US.utf-8 && rm -rf packages && ./contrib/make_packages && ./contrib/make_apk'
