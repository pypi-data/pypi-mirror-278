#!/bin/bash

# $1 - a request: '?' - list hardware, '!' - execute the command.
# $2 - a hardware entry to use, if there are multiple.
# $@ - a command to run as separate tokens.

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
    echo "Hardware: $2"
    LIST=("${@:3}")
    if [[ -z "${LIST[@]}" ]]; then
        # TODO: Start an interactive session.
        echo "Interactive"
    else
        # TODO: Run the command.
        for ITEM in "${LIST[@]}"; do
            printf "%s\n" "${ITEM}"
        done
    fi
fi
