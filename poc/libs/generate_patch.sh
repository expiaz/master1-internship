#!/bin/bash

if [ $# -eq 0 ]; then
    target="mirage"
else
    target=$1
fi

if [ -d "$target" ]; then
    cd "$target"
    git add *
    git diff HEAD > "../$target.patch"
    echo "patch generated at $target.patch"
else
    echo "run 'git submodule init' first"
fi