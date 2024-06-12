##########################################################################################
# textkernel/tests/test_value.py
##########################################################################################

import datetime as dt
import unittest

from pyparsing                import StringEnd, ParseException
from textkernel._DATA_GRAMMAR import VALUE, OPT_WHITE


class Test_VALUE_GRAMMAR(unittest.TestCase):

    def test_INT(self):
        p = VALUE + OPT_WHITE + StringEnd()
        self.assertEqual(p.parse_string('  1234 ')[0],  1234)
        self.assertEqual(p.parse_string(' -1234 ')[0], -1234)
        self.assertEqual(p.parse_string(' +1234 ')[0],  1234)

    def test_FLOAT(self):
        p = VALUE + OPT_WHITE + StringEnd()
        self.assertEqual(p.parse_string('  1234.      ')[0],  1234.)
        self.assertEqual(p.parse_string('  12340.e-01 ')[0],  1234.)
        self.assertEqual(p.parse_string('  12340e-1   ')[0],  1234.)
        self.assertEqual(p.parse_string('  234.5e+01  ')[0],  2345.)
        self.assertEqual(p.parse_string('  234.5D1    ')[0],  2345.)
        self.assertEqual(p.parse_string('  234.5d1    ')[0],  2345.)
        self.assertEqual(p.parse_string('  234.5E+001 ')[0],  2345.)
        self.assertEqual(p.parse_string(' +1234.      ')[0],  1234.)
        self.assertEqual(p.parse_string(' +12340.e-01 ')[0],  1234.)
        self.assertEqual(p.parse_string(' +12340e-1   ')[0],  1234.)
        self.assertEqual(p.parse_string(' +234.5e+01  ')[0],  2345.)
        self.assertEqual(p.parse_string(' +234.5D1    ')[0],  2345.)
        self.assertEqual(p.parse_string(' +234.5d1    ')[0],  2345.)
        self.assertEqual(p.parse_string(' +234.5E+001 ')[0],  2345.)
        self.assertEqual(p.parse_string(' -1234.0     ')[0], -1234.)
        self.assertEqual(p.parse_string(' -12340.e-01 ')[0], -1234.)
        self.assertEqual(p.parse_string(' -12340e-1   ')[0], -1234.)
        self.assertEqual(p.parse_string(' -234.5e+01  ')[0], -2345.)
        self.assertEqual(p.parse_string(' -234.5D1    ')[0], -2345.)
        self.assertEqual(p.parse_string(' -234.5d1    ')[0], -2345.)
        self.assertEqual(p.parse_string(' -234.5E+001 ')[0], -2345.)

        self.assertRaises(ParseException, p.parse_string, '  1234 .  ')
        self.assertRaises(ParseException, p.parse_string, '- 12340e-1')
        self.assertRaises(ParseException, p.parse_string, '-12340 e-1')
        self.assertRaises(ParseException, p.parse_string, '-12340e -1')
        self.assertRaises(ParseException, p.parse_string, '-12340e- 1')

    def test_STRING(self):
        p = VALUE + OPT_WHITE + StringEnd()
        self.assertEqual(p.parse_string(" '  1234 '")[0], "  1234 ")
        self.assertEqual(p.parse_string("''' 1234 '")[0], "' 1234 ")
        self.assertEqual(p.parse_string("' 1234 '''")[0], " 1234 '")
        self.assertEqual(p.parse_string("' 12''34 '")[0], " 12'34 ")
        self.assertEqual(p.parse_string("''")[0],         "")
        self.assertEqual(p.parse_string("''''")[0],       "'")

    def test_DATE(self):
        p = VALUE + OPT_WHITE + StringEnd()
        self.assertEqual(p.parse_string('@2001-Jan-01')[0], dt.datetime(2001,1,1))
        self.assertEqual(p.parse_string('@2001-Jan-01:12:34:56.789')[0],
                         dt.datetime(2001,1,1,12,34,56,789000))

        self.assertRaises(ParseException, p.parse_string, '@ 2001-Jan-01')
        self.assertRaises(Exception, p.parse_string, '@2001 -Jan-01')
        self.assertRaises(Exception, p.parse_string, '@2001- Jan-01')

    def test_LIST(self):
        p = VALUE + OPT_WHITE + StringEnd()
        self.assertEqual(p.parse_string('(1,2,3)')[0],    [1,2,3])
        self.assertEqual(p.parse_string('(1)')[0],        1)
        self.assertEqual(p.parse_string('(1,2, \n3)')[0], [1,2,3])
        self.assertEqual(p.parse_string("('1','2')")[0],  ['1','2'])
        self.assertEqual(p.parse_string("('1''','2')")[0],["1'","2"])
        self.assertEqual(p.parse_string('(1, @Jul-4-1776)')[0],
                         [1, dt.datetime(1776,7,4)])


##########################################################################################
# Perform unit testing if executed from the command line
##########################################################################################

if __name__ == '__main__':
    unittest.main()

##########################################################################################
