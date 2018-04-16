import unittest
import keymap

class TestKeymap(unittest.TestCase):

  def test_key_code(self):
    self.assertEqual(keymap.get_key_code('a'), 0x700000004)
    self.assertEqual(keymap.get_key_code('rightctrl'), 0x7000000e4)

  def test_key_name(self):
    self.assertEqual(keymap.get_key_name(0x700000004), 'a')
    self.assertEqual(keymap.get_key_name(0x7000000e4), 'rightctrl')

  def test_remove_dups(self):
    akey = keymap.get_key_code('a')
    bkey = keymap.get_key_code('b')
    ckey = keymap.get_key_code('c')
    list_with_dups = [keymap.key_mapping(bkey, akey),
        keymap.key_mapping(bkey, ckey),
        keymap.key_mapping(akey, bkey),
        keymap.key_mapping(akey, ckey)]
    list_without_dups = [keymap.key_mapping(bkey, ckey),
        keymap.key_mapping(akey, ckey)]
    self.assertEqual(keymap.remove_dups(list_with_dups), list_without_dups)
      # remove_dups should remove duplicate src entries and retain the latest
      # in the list

  def test_format_list_item(self):
    akey = keymap.get_key_code('a')
    bkey = keymap.get_key_code('b')
    item = keymap.key_mapping(akey, bkey)
    listitem = keymap.format_list_item(item)
    self.assertEqual(listitem, '{"HIDKeyboardModifierMappingSrc":0x700000004,"HIDKeyboardModifierMappingDst":0x700000005}')

  def test_format_mappings_for_setting(self):
    expected = '{"UserKeyMapping":[{"HIDKeyboardModifierMappingSrc":0x700000004,"HIDKeyboardModifierMappingDst":0x700000005},{"HIDKeyboardModifierMappingSrc":0x700000005,"HIDKeyboardModifierMappingDst":0x700000004}]}'
    akey = keymap.get_key_code('a')
    bkey = keymap.get_key_code('b')
    self.assertEqual(keymap.format_mappings_for_setting([
      keymap.key_mapping(akey, bkey), keymap.key_mapping(bkey, akey)]),
      expected)

  def test_parse_mappings(self):
    sys_output = """
(
        {
        HIDKeyboardModifierMappingDst = 30064771129;
        HIDKeyboardModifierMappingSrc = 30064771113;
    },
        {
        HIDKeyboardModifierMappingDst = 30064771113;
        HIDKeyboardModifierMappingSrc = 30064771129;
    }
)
"""
    esc = keymap.get_key_code('escape')
    caps = keymap.get_key_code('caps')
    self.assertEqual(keymap.parse_mappings(sys_output),
        [keymap.key_mapping(esc, caps), keymap.key_mapping(caps, esc)])

  def test_remove_keys(self):
    esc = keymap.get_key_code('escape')
    akey = keymap.get_key_code('a')
    tab = keymap.get_key_code('tab')
    mappings = [keymap.key_mapping(esc, akey), keymap.key_mapping(akey, tab),
        keymap.key_mapping(tab, esc)]
    self.assertEqual(keymap.remove_keys(mappings, [akey, tab]),
        [keymap.key_mapping(esc, akey)])

if __name__ == '__main__':
  unittest.main()
