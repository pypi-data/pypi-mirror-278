#!/bin/bash

# $1 - a request: '?' - list components, '!' - execute the command.
# $@ - a list of components. If empty, the entire workspace is assumed.

set -e
ROOT="$(realpath $(dirname "${BASH_SOURCE[0]}")/..)"

if [[ $1 == '?' ]]; then
    # TODO: Populate the components, if any.
    LIST=()
    for ITEM in "${LIST[@]}"; do
        echo ${ITEM}
    done
fi

if [[ $1 == '!' ]]; then
    LIST=(${@:2})
    if [[ -z "${LIST[*]}" ]]; then
        # TODO: Execute for the workspace.
        echo "Workspace"
    else
        for ITEM in "${LIST[@]}"; do
            # TODO: Execute for the component.
            echo "Component ${ITEM}"
        done
    fi
fi
