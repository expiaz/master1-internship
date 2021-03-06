#!/bin/sh

if [ $# -eq 0 ]; then
    target="mirage"
else
    target=$1
fi

if [ -f "$target.patch" ]; then
    cd "$target"
    git apply "../$target.patch"
    echo "patch applied from $target.patch to $target"
else
    echo "run 'git submodule init and git submodule update' first"
fi