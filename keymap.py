#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os
import subprocess
import textwrap
import platform

if platform.mac_ver()[0] == '' or int(
    platform.mac_ver()[0].split('.')[1]) < 12:
  print("This tool requires macOS >= 10.12")
  exit(1)

keys = ("a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8"
        " 9 0 return escape delete tab space - = [ ] \ # ; ' ` , . / caps f1"
        " f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 printscreen brightness-"
        " brightness+ insert home pageup deleteforward end pagedown right"
        " left down up numlock keypad/ keypad* keypad- keypad+ keypadenter"
        " keypad1 keypad2 keypad3 keypad4 keypad5 keypad6 keypad7 keypad8"
        " keypad9 keypad0 keypad. non-us| application power keypad= f13 f14"
        " f15 f16 f17 f18 f19 f20 f21 f22 f23 f24 execute help menu select"
        " stop again undo cut copy paste find mute volume+ volume-").split(' ')

keys.extend([None] * 94) # codes 130--223

keys.extend("leftctrl leftshift leftalt leftcmd rightctrl rightshift rightalt"
        " rightcmd".split(' '))

def show_help():
  print("""Usage:
{0} map <key> <dest> # Map <key> to <dest>
{0} swap <key> <key> # Swap two keys
{0} unmap <keys>... # Remove one or more mappings
{0} list # List current key mappings
{0} keys # Show key names""".format(sys.argv[0]))

def key_names():
  print('\n'.join(textwrap.wrap(' '.join([key for key in keys if key is not None]))))

def get_key_code(key):
  return (0x700000000 | keys.index(key) + 4) if key in keys else None

def get_key_name(code):
  return keys[(0x700000000 ^ int(code)) - 4]

def print_mappings(mappings):
  for mapping in mappings:
    print("%s -> %s" % (get_key_name(mapping['src']),
      get_key_name(mapping['dst'])))

def remove_dups(mappings):
  seen = []
  unique = []
  mappings.reverse()
  for mapping in mappings:
    if int(mapping['src']) not in seen:
      unique.append(mapping)
      seen.append(mapping['src'])
  unique.reverse()
  return unique

def get_mappings():
  out = subprocess.check_output(["hidutil", "property", "--get",
    "UserKeyMapping"]).decode("utf-8")
  parsed_mappings = re.findall(r'(?:{\s*HIDKeyboardModifierMappingDst = ([0-9]+);\s*'
    'HIDKeyboardModifierMappingSrc = ([0-9]+);\s*}|{\s*'
    'HIDKeyboardModifierMappingSrc = ([0-9]+);\s*HIDKeyboardModifierMappingDst'
    '= ([0-9]+);\s*})', out)
  mappings = []
  for mapping in parsed_mappings:
    if mapping[0] == '':
      mappings.append({ 'src': mapping[2], 'dst': mapping[3] })
    else:
      mappings.append({ 'src': mapping[1], 'dst': mapping[0] })
  return mappings

def set_mappings(mappings):
  key_mapping = ('{"UserKeyMapping":['
      + ','.join(list(map(format_list_item, mappings))) + ']}')
  with open(os.devnull, 'w') as devnull:
    code = subprocess.check_call(["hidutil", "property", "--set", key_mapping],
        stdout=devnull)
  if code == 0:
    print_mappings(mappings)
  exit(code)

def format_list_item(mapping):
  return ('{"HIDKeyboardModifierMappingSrc":0x%02x,'
          '"HIDKeyboardModifierMappingDst":0x%02x}' % (int(mapping['src']),
          int(mapping['dst'])))

def unmap(key_args):
  key_args = list(map(get_key_code, key_args))
  mappings = [mapping for mapping in get_mappings() if int(mapping['src']) not in key_args]
  set_mappings(mappings)

def key_mapping(src, dst):
  return { 'src': src, 'dst': dst }

def map_keys(key1, key2, swap=False):
  src = get_key_code(key1)
  dst = get_key_code(key2)
  if src is not None and dst is not None:
    mappings = get_mappings()
    mappings.append(key_mapping(src, dst))
    if swap:
      mappings.append(key_mapping(dst, src))
    mappings = remove_dups(mappings)
    #print_mappings(mappings)
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
    print_mappings(get_mappings())
  elif command == 'keys':
    key_names()
  elif command == 'map' and key_count == 2:
    map_keys(key_args[0], key_args[1])
  elif command == 'swap' and key_count == 2:
    map_keys(key_args[0], key_args[1], True)
  elif command == 'help':
    show_help()
  elif command == 'unmap' and key_count >= 1:
    unmap(key_args)
  else:
    show_help()
    exit(1)
