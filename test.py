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

if __name__ == '__main__':
  unittest.main()
