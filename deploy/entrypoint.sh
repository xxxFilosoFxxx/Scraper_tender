#!/bin/bash

cd /usr/share/python3
. venv/bin/activate

read -r -p "Search tender key: " SEARCH_KEY
if [[ "${SEARCH_KEY}" == "" ]]
then
    echo "Error: search key must be specify"
    exit 1
fi

export SEARCH_KEY="${SEARCH_KEY}"

python ./parse_sber_ats.py