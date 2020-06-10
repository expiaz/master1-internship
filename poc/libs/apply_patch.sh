#!/bin/bash

if [ $# -eq 0 ]; then
    target="mirage"
else
    target=$1
fi

if [ -f "$target.patch" ]; then
    cd "$target"
    git stash push
    git apply "../$target.patch"
    echo "patch applied from $target.patch to $target"
else
    echo "run 'git submodule init' first"
fi