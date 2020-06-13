#!/bin/sh

rat=$(pwd)
echo "generate patch pwd: $rat"

if [ $# -eq 0 ]; then
    target="mirage"
else
    target=$1
fi

if [ -d "$target" ]; then
    cd "$target"
    git diff HEAD > "../$target.patch"
    echo "patch generated at $target.patch"
else
    echo "run 'git submodule init' first"
fi