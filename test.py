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
    self.assertEqual(keymap.remove_dups(
      [{'src':0x700000004,'dst':0x7000000e4},
       {'src':0x700000004,'dst':0x7000000d4}]),
      # remove_dups should remove duplicate src entries and retain the latest
      # in the list
      [{'src':0x700000004,'dst':0x7000000d4}])

if __name__ == '__main__':
  unittest.main()
