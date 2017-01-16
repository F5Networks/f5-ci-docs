#!/usr/bin/env bash

set -x

echo "Checking grammar and style"
write-good `find ./docs -name '*.rst'` --no-passive --so --illusion --thereIs || true

echo "Building docs and checking links with Sphinx"
mkdir -p ./docs/test
touch ./docs/test/sphinx-build.output
sphinx-build -aE -b html -b linkcheck -w ./docs/test/sphinx-build.output ./docs ./docs/test

echo "The errors listed below must be fixed."
! ack-grep --pager=cat '.*(ERROR: .+|SEVERE: .+|Exception: .+)|.*(WARNING: (?!toctree|document|duplicate).+)' ./docs/test/sphinx-build.output
! ack-grep --pager=cat '^(InputError:.*)|^.*(\[broken\].+|\[redirected .+\]*+)' ./docs/test/output.txt

