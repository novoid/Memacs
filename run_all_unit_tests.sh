#!/bin/sh
# Run the full unit test suite via uv.
# Requires `uv` on PATH (https://docs.astral.sh/uv/).

set -e

cd "$(dirname "$0")"

uv run --group dev pytest --exitfirst memacs/tests memacs/lib/tests "$@"

#end
