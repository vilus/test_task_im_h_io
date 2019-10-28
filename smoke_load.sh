#!/usr/bin/env bash

FLOWS=10
REQS=100

function do_reqs {
    for i in $( seq ${REQS} )
    do
        curl -s -i -H "Content-Type: application/json; charset=utf-8" \
            -X POST -d '{"user_action":"3","feedback":"hi"}' 127.0.0.1:58001/nps \
            | grep -Pzo "(400 Bad Request)(.|\n)*"
    done
}

for i in $( seq ${FLOWS} )
do
    do_reqs &
done

wait
