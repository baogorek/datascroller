#! /usr/bin/env bash

function install_test_requirements(){
    pip install -r ./test_requirements.txt
}

function run_test(){
    flake8 \
    --max-line-length 160 \
    ./datascroller
}

main() {
    install_test_requirements
    run_test
}

main
