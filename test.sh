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

expected_user_key_mapping=$(cat <<'EOF'
(
        {
        HIDKeyboardModifierMappingDst = 30064771113;
        HIDKeyboardModifierMappingSrc = 30064771129;
    },
        {
        HIDKeyboardModifierMappingDst = 30064771129;
        HIDKeyboardModifierMappingSrc = 30064771113;
    }
)
EOF
)

if [ "$expected_user_key_mapping" != "$(hidutil property --get UserKeyMapping)" ]; then
  echo "hidutil UserKeyMapping did not match expected value"
  echo "Expected: $expected_user_key_mapping"
  echo "Actual: $(hidutil property --get UserKeyMapping)"
  exit 1
fi

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
