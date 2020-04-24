#!/usr/local/bin/bash

if [ "$#" -lt 1 ]; then
	echo $0 <output file>.pdf [<template>]
	exit 1
fi

SRC_FMT="markdown_github-auto_identifiers+yaml_metadata_block+smart"
OUT_FMT="pdf"

OUT_FILE=$1
INDEX="index"
TEMPLATE=${2:-ubs.tex}
DATA_DIR=$(pwd)

pandoc -s -o "$OUT_FILE.pdf" -f "$SRC_FMT" -t "$OUT_FMT" \
	--data-dir="$DATA_DIR" --template "$TEMPLATE" \
	$(cat "$INDEX")
