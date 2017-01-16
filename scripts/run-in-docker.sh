#!/usr/bin/env bash

IMGNAME=thejodesterf5/containthedocs
IMGTAG=latest

set -x

exec docker run --rm -it -v $PWD:$PWD --workdir $PWD -e "LOCAL_USER_ID=$(id -u)" ${IMGNAME}:${IMGTAG} "$@"
