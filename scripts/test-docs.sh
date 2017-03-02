#!/usr/bin/env bash

set -x

set -e

# Pip install the requirements file
pip install -r requirements.txt

echo "Building docs and checking links with Sphinx"
make -C docs clean
make -C docs html
make -C docs linkcheck

echo "Checking grammar and style"
write-good docs/*.rst --weasel --so --passive --illusion --thereIs --toowordy --adverb --cliches

