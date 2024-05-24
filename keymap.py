#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import os
import subprocess
import textwrap
import platform

if platform.mac_ver()[0] == '' or (
    int(platform.mac_ver()[0].split('.')[0]) <= 10
        and int(platform.mac_ver()[0].split('.')[1]) < 12):
  print("This tool requires macOS >= 10.12")
  exit(1)

keys = [None] * 4

keys.extend(("a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8"
        " 9 0 return escape delete tab space - = [ ] \\ # ; ' ` , . / caps f1"
        " f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 printscreen brightness-"
        " brightness+ insert home pageup deleteforward end pagedown right"
        " left down up numlock keypad/ keypad* keypad- keypad+ keypadenter"
        " keypad1 keypad2 keypad3 keypad4 keypad5 keypad6 keypad7 keypad8"
        " keypad9 keypad0 keypad. non-us| application power keypad= f13 f14"
        " f15 f16 f17 f18 f19 f20 f21 f22 f23 f24 execute help menu select"
        " stop again undo cut copy paste find mute volume+ volume-").split(' '))

keys.extend([None] * 94) # codes 130--223

keys.extend("leftctrl leftshift leftalt leftcmd rightctrl rightshift rightalt"
        " rightcmd".split(' '))

def show_help():
  print("""Usage:
{0} map <key> <dest> # Map <key> to <dest>
{0} swap <key> <key> # Swap two keys
{0} unmap <keys>... # Remove one or more mappings
{0} list # List current key mappings
{0} save [file] # Save your mappings to file (default is ~/.keymaprc)
{0} load [file] # Load your mappings from file (default is ~/.keymaprc)
{0} keys # Show key names""".format(os.path.basename(__file__)))

def key_names():
  print('\n'.join(textwrap.wrap(' '.join([key for key in keys if key is not None]))))

def get_key_code(key):
  return (0x700000000 | keys.index(key)) if key in keys else None

def get_key_name(code):
  return keys[(0x700000000 ^ int(code))]

def format_mapping_for_print(mapping):
  return ("%s -> %s" % (get_key_name(mapping['src']),
      get_key_name(mapping['dst'])))

def save_mappings(filename=None):
  if filename is None:
    filename = os.path.join(os.path.expanduser('~'), '.keymaprc')
  mappings = get_system_mappings()
  if len(mappings) > 0:
    with open(filename, 'w') as rcfile:
      for mapping in mappings:
        rcfile.write(format_mapping_for_print(mapping) + '\n')
    print("Saved to " + filename + ":")
    print_mappings(mappings)
  else:
    print("No mappings to save!")
    exit(1)

def load_mappings(filename=None):
  if filename is None:
    filename = os.path.join(os.path.expanduser('~'), '.keymaprc')
  if os.path.isfile(filename):
    mappings = []
    with open(filename, 'r') as rcfile:
      for line in rcfile:
        match = re.search(r'^(\S+) -> (\S+)$', line)
        if match:
          key1 = match.group(1)
          key2 = match.group(2)
          src = get_key_code(key1)
          dst = get_key_code(key2)
          if src is not None and dst is not None:
            mappings.append(key_mapping(src, dst))
          else:
            print("Invalid key: %s" % (key1 if src is None else key2))
    mappings = remove_dups(mappings)
    print("Loaded from " + filename + ":")
    set_mappings(mappings)
  else:
    print("Could not read file: " + filename)
    exit(1)

def print_mappings(mappings):
  for mapping in mappings:
    print(format_mapping_for_print(mapping))

def remove_dups(mappings):
  seen = []
  unique = []
  mappings.reverse()
  for mapping in mappings:
    if mapping['src'] not in seen:
      unique.append(mapping)
      seen.append(mapping['src'])
  unique.reverse()
  return unique

def parse_mappings(sys_output):
  parsed = re.findall(r'{\s*HIDKeyboardModifierMapping(Dst|Src) ='
    r' ([0-9]+);\s*' r'HIDKeyboardModifierMapping(Dst|Src) = ([0-9]+);\s*}',
    sys_output)
  mappings = []
  for mapping in parsed:
    mappings.append({ mapping[0].lower(): int(mapping[1]),
      mapping[2].lower(): int(mapping[3]) })
  return mappings

def get_system_mappings():
  out = subprocess.check_output(["hidutil", "property", "--get",
    "UserKeyMapping"]).decode("utf-8")
  return parse_mappings(out)

def format_mappings_for_setting(mappings):
  return ('{"UserKeyMapping":['
      + ','.join(list(map(format_list_item, mappings))) + ']}')

def set_mappings(mappings):
  key_mapping = format_mappings_for_setting(mappings)
  with open(os.devnull, 'w') as devnull:
    code = subprocess.check_call(["hidutil", "property", "--set", key_mapping],
        stdout=devnull)
  if code == 0:
    print_mappings(mappings)
  exit(code)

def format_list_item(mapping):
  return ('{"HIDKeyboardModifierMappingSrc":0x%02x,'
          '"HIDKeyboardModifierMappingDst":0x%02x}' % (mapping['src'],
          mapping['dst']))

def remove_keys(mappings, key_args):
  mappings = [mapping for mapping in mappings if int(mapping['src']) not in key_args]
  return mappings

def unmap(key_args):
  key_args = list(map(get_key_code, key_args))
  mappings = remove_keys(get_system_mappings(), key_args)
  set_mappings(mappings)

def key_mapping(src, dst):
  return { 'src': int(src), 'dst': int(dst) }

def map_keys(key1, key2, swap=False):
  src = get_key_code(key1)
  dst = get_key_code(key2)
  if src is not None and dst is not None:
    mappings = get_system_mappings()
    mappings.append(key_mapping(src, dst))
    if swap:
      mappings.append(key_mapping(dst, src))
    mappings = remove_dups(mappings)
    set_mappings(mappings)
  else:
    print("Invalid key: %s" % (key1 if src is None else key2))
    exit(1)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    show_help()
    exit(1)

  command = sys.argv[1]

  key_args = sys.argv[2:]
  key_count = len(key_args)

  if command == 'list':
    print_mappings(get_system_mappings())
  elif command == 'keys':
    key_names()
  elif command == 'map' and key_count == 2:
    map_keys(key_args[0], key_args[1])
  elif command == 'swap' and key_count == 2:
    map_keys(key_args[0], key_args[1], True)
  elif command == 'help':
    show_help()
  elif command == 'save':
    save_mappings(None if key_count == 0 else key_args[0])
  elif command == 'load':
    load_mappings(None if key_count == 0 else key_args[0])
  elif command == 'unmap' and key_count >= 1:
    unmap(key_args)
  else:
    show_help()
    exit(1)
