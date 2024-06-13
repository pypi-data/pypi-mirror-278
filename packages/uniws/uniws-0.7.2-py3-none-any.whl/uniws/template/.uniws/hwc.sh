#!/bin/bash

# $1 - a request: '?' - list hardware, '!' - execute the command, '@' - list states.
# $2 - a hardware entry to use, if there are multiple.
# $3 - a state to use.

set -e
ROOT="$(realpath $(dirname "${BASH_SOURCE[0]}")/..)"

if [[ $1 == '?' ]]; then
    # TODO: Populate the hardware, if any.
    LIST=()
    for ITEM in "${LIST[@]}"; do
        echo ${ITEM}
    done
fi

if [[ $1 == '@' ]]; then
    # TODO: Populate the states.
    LIST=(
        'switch Change the connection state.'
        'attach Connect to the hardware.'
        'detach Disconnect from the hardware.'
    )
    for ITEM in "${LIST[@]}"; do
        echo ${ITEM}
    done
fi

if [[ $1 == '!' ]]; then
    # TODO: Set state approprietly.
    echo "Hardware: $2"
    if [[ $3 == 'switch' ]]; then
        echo 'Switch'
    fi
    if [[ $3 == 'attach' ]]; then
        echo 'Attach'
    fi
    if [[ $3 == 'detach' ]]; then
        echo 'Detach'
    fi
fi
