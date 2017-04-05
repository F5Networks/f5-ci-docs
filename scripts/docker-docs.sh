#!/usr/bin/env bash

set -x

exec docker run --rm -it -v $PWD:$PWD --workdir $PWD -e "LOCAL_USER_ID=$(id -u)" f5devcentral/containthedocs "$@"
