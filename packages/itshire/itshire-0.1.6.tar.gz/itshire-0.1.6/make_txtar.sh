#!/usr/bin/env bash
set -e

tmp=$(mktemp -d itshire.XXXXX)

if [ -z "${tmp+x}" ] || [ -z "$tmp" ]; then
    echo "error: $tmp is not set or is an empty string."
    exit 1
fi

if ! command -v txtar-c >/dev/null; then
    echo go install github.com/rogpeppe/go-internal/cmd/txtar-c@latest
	exit 1
fi

declare -a files=(
	# .gitignore # loc: 12
	# .pytest_cache/.gitignore # loc: 2
	# .pytest_cache/CACHEDIR.TAG # loc: 4
	# .pytest_cache/README.md # loc: 8
	# .pytest_cache/v/cache/nodeids # loc: 3
	# .pytest_cache/v/cache/stepwise # loc: 1
	# Makefile # loc: 3
	# README.md # loc: 5
	# itshire.code-workspace # loc: 8
	# main.py # loc: 38
	# make_txtar.sh # loc: 60
	# parse_section_headers.py # loc: 27
	# pyproject.toml # loc: 37
	# requirements-dev.lock # loc: 45
	# requirements-test.txt # loc: 1
	# requirements.lock # loc: 21
	# requirements.txt # loc: 1
	src/itshire/__init__.py # loc: 18
	src/itshire/__main__.py # loc: 5
	src/itshire/add_frontmatter.py # loc: 20
	src/itshire/add_sections.py # loc: 73
	# src/itshire/cli.py # loc: 20
	# src/itshire/log.py # loc: 9
	# src/itshire/main2.py # loc: 15
	# src/itshire/templates/base.j2 # loc: 3
	# src/itshire/templates/extended.j2 # loc: 3
	# test.md # loc: 23
	# tests/test_add_sections.py # loc: 18
	
)
for file in "${files[@]}"; do
    echo $file
done | tee $tmp/filelist.txt

tar -cf $tmp/itshire.tar -T $tmp/filelist.txt
mkdir -p $tmp/itshire
tar xf $tmp/itshire.tar -C $tmp/itshire
rg --hidden --files $tmp/itshire

mkdir -p $tmp/gpt_instructions_XXYYBB

cat >$tmp/gpt_instructions_XXYYBB/1.txt <<EOF

EOF

{
    cat $tmp/gpt_instructions_XXYYBB/1.txt
    echo txtar archive is below
    txtar-c -quote -a $tmp/itshire
} | pbcopy

rm -rf $tmp
