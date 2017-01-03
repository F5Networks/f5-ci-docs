#!/usr/bin/env bash

echo "Building documentation with sphinx."
sphinx-build -aEQ ./docs/ ./docs/_build

echo "The documentation has been built. Open /docs/_build/index.html in a browser to view it."

echo "Checking grammar and style"
exec write-good `find ./docs -name '*.rst'` --no-passive --so --illusion --thereIs || true

