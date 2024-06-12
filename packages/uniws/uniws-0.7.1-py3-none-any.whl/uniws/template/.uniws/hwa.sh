#!/bin/bash

# $1 - a request: '?' - list hardware, '!' - execute the command.
# $2 - a hardware entry to use, if there are multiple.

set -e
ROOT="$(realpath $(dirname "${BASH_SOURCE[0]}")/..)"

if [[ $1 == '?' ]]; then
    # TODO: Populate the hardware, if any.
    LIST=()
    for ITEM in "${LIST[@]}"; do
        echo ${ITEM}
    done
fi

if [[ $1 == '!' ]]; then
    # TODO: Perform an action.
    echo "Hardware: $2"
fi
