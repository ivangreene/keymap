#!/usr/bin/env bash
set -e

# Save and unmap current user mappings
./keymap.py save tmp.keymaprc
./keymap.py list | cut -d ' ' -f 1 | xargs -n1 ./keymap.py unmap

./keymap.py list | wc -l | grep 0

./keymap.py swap caps escape
./keymap.py list | grep 'caps -> escape'
./keymap.py list | grep 'escape -> caps'
./keymap.py list | wc -l | grep 2

./keymap.py save

cat ~/.keymaprc | grep 'caps -> escape'
cat ~/.keymaprc | grep 'escape -> caps'
cat ~/.keymaprc | wc -l | grep 2

./keymap.py unmap caps escape
./keymap.py list | wc -l | grep 0

./keymap.py load
./keymap.py list | grep 'caps -> escape'
./keymap.py list | grep 'escape -> caps'
./keymap.py list | wc -l | grep 2

# Unmap test mappings, load stored user mappings
./keymap.py unmap caps escape
./keymap.py load tmp.keymaprc
rm tmp.keymaprc
