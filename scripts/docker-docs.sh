#!/usr/bin/env bash

set -x

: ${DOC_IMG:=f5devcentral/containthedocs:1.0.8}

exec docker run --rm -it \
  -v $PWD:$PWD --workdir $PWD \
  ${DOCKER_RUN_ARGS} \
  -e "LOCAL_USER_ID=$(id -u)" \
  ${DOC_IMG} "$@"
