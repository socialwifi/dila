#!/bin/bash
DIRECTORY="$(dirname "${BASH_SOURCE[0]}")"
MAIN_DIRECTORY=$(pushd $Directory > /dev/null; git rev-parse --show-toplevel; popd > /dev/null)
tar ch --hard-dereference --exclude=__pycache__ --mode="g=u,o=rX" --owner=root --group=root \
    -C $DIRECTORY ./ \
    -C $MAIN_DIRECTORY . \
| docker build --tag $1 -
