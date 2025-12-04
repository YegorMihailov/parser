import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import get_voyager_date, get_rfc_date, get_brain_emoji, get_btc_date, get_ISBN_10
import unittest


class TestMySolution(unittest.TestCase):

  def test(self):
    """Check the correctness of extracted data"""
    self.assertEqual(get_voyager_date(), "19770905")
    self.assertEqual(get_rfc_date(), "19900401")
    self.assertEqual(get_brain_emoji(), "1F9E0")
    self.assertEqual(get_btc_date(), "20090103")
    self.assertEqual(get_ISBN_10(), "0131103628")

if __name__ == '__main__':
  unittest.main()