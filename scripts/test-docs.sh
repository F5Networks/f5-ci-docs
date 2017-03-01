#!/usr/bin/env bash

set -x

set -e

pip install git+https://github.com/f5devcentral/f5-sphinx-theme.git@master

echo "Building docs and checking links with Sphinx"
rm -rf docs/_build
make -C docs html
make -C docs linkcheck

echo "Checking grammar and style"
write-good docs/*.rst --weasel --so --passive --illusion --thereIs --toowordy --adverb --cliches

