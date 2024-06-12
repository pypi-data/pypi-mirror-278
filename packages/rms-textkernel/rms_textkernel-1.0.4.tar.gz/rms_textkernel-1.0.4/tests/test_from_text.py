##########################################################################################
# textkernel/tests/test_from_text.py
##########################################################################################

import unittest

from pyparsing  import ParseException
from textkernel import from_text, continued_value


class Test_from_text(unittest.TestCase):

    ##########################################

    def test_continued_strings(self):

        text = """
            CONTINUED_STRINGS = ( 'This //  ',
                                  'is //  ',
                                  'just //',
                                  'one long //',
                                  'string.',
                                  'Here''s a second //',
                                  'continued //'
                                  'string.'              )
        """
        d = from_text(text, contin='//', commented=False)
        self.assertEqual(d, {'CONTINUED_STRINGS': [
                                'This is just one long string.',
                                "Here's a second continued string."]})

        parts = text.split('\n')
        d = from_text(parts, contin='//', commented=False)
        self.assertEqual(d, {'CONTINUED_STRINGS': [
                                'This is just one long string.',
                                "Here's a second continued string."]})

        # Collapse one-element list to a string
        d = from_text("""
            CONTINUED_STRINGS = ( 'This //  ',
                                  'is //  ',
                                  'just //',
                                  'one long //',
                                  'string.' )
            """, contin='//', commented=False)
        self.assertEqual(d, {'CONTINUED_STRINGS':  'This is just one long string.'})

        # No continuation specified
        d = from_text("""
            CONTINUED_STRINGS = ( 'This //  ',
                                  'is //  ',
                                  'just //',
                                  'one long //',
                                  'string.' )
            """, commented=False)
        self.assertEqual(d, {'CONTINUED_STRINGS': ['This //  ', 'is //  ', 'just //',
                                                   'one long //', 'string.']})

        # "+" is the default sequence for metakernels
        d = from_text("""
            KERNELS_TO_LOAD = (
            'sat164.+',
            'b+    '
            'sp',
            'naif0012.tls'  )
        """, commented=False)
        self.assertEqual(d, {'KERNELS_TO_LOAD': ['sat164.bsp', 'naif0012.tls']})

        # Different continuations
        d = from_text("""
            KERNELS_TO_LOAD = (
            'sat164.+',
            'b+    '
            'sp',
            'naif0012.tls'  )
            CONTINUED_STRINGS = ( 'This //  ',
                                  'is //  ',
                                  'just //',
                                  'one long //',
                                  'string.',
                                  'Here''s a second //',
                                  'continued //'
                                  'string.'              )
            """, contin='//', commented=False)
        self.assertEqual(d, {'KERNELS_TO_LOAD': ['sat164.+', 'b+    ', 'sp',
                                                 'naif0012.tls'],
                             'CONTINUED_STRINGS': ['This is just one long string.',
                                                   "Here's a second continued string."]})
        self.assertEqual(continued_value(d['KERNELS_TO_LOAD'], '+'),
                         ['sat164.bsp', 'naif0012.tls'])

    ##########################################

    def test_continued_value(self):

        val = ['sat164.+', 'b+    ', 'sp', 'naif0012.tls']
        self.assertEqual(continued_value(val, '+'), ['sat164.bsp', 'naif0012.tls'])

        val = ['sat164.+', 'b+    ', 'sp+', 77]
        self.assertEqual(continued_value(val, '+'), ['sat164.bsp+', 77])

        val = ['sat164.+', 'b+    ', 'sp']
        self.assertEqual(continued_value(val, '+'), 'sat164.bsp')

        val = ['sat164.+', 'b+    ', 'sp+']
        self.assertEqual(continued_value(val, '+'), 'sat164.bsp+')

        val = ['sat164. CONTINUATION!', 'b CONTINUATION!    ', 'sp CONTINUATION! ']
        self.assertEqual(continued_value(val, ' CONTINUATION!'),
                         'sat164.bsp CONTINUATION! ')

        val = ['sat164.bsp', 'naif0012.tls']
        self.assertIs(continued_value(val, '+'), val)

        val = ['sat164.bsp']    # no change, so no collapse
        self.assertIs(continued_value(val, '+'), val)

        val = ['sat164.bsp+']
        self.assertIs(continued_value(val, '+'), val)

        val = 'sat164.bsp+'
        self.assertIs(continued_value(val, '+'), val)

        self.assertEqual(continued_value(777, '+'), 777)
        self.assertIsInstance(continued_value(777, '+'), int)

        self.assertEqual(continued_value(777., '+'), 777.)
        self.assertIsInstance(continued_value(777., '+'), float)

        val = [1, 2, 3.]
        self.assertIs(continued_value(val, '+'), val)

    ##########################################

    def test_plus_equal(self):

        d = from_text("""
            VAL = ( 1 )
        """, commented=False)
        self.assertEqual(d['VAL'], 1)

        d = from_text("""
            VAL += ( 1 )
        """, commented=False)
        self.assertEqual(d['VAL'], [1])

        d = from_text("""
            VAL = 1
            VAL += (  2)
        """, commented=False)
        self.assertEqual(d['VAL'], [1,2])

        d = from_text("""
            VAL = 1
            VAL +=   2
        """, commented=False)
        self.assertEqual(d['VAL'], [1,2])

        d = from_text("""
            VAL = 1
            VAL += (  2 3)
        """, commented=False)
        self.assertEqual(d['VAL'], [1,2,3])

        d = from_text("""
            VAL = (1   2)
            VAL += 3
        """, commented=False)
        self.assertEqual(d['VAL'], [1,2,3])

        # No continuation of separate entries
        d = from_text("""
            VAL = 'abc+'
            VAL += 'def'
        """, commented=False, contin='+')
        self.assertEqual(d['VAL'], ['abc+', 'def'])

    ##########################################

    def test_commented(self):

        text = r"""

            Explanatory text about how to use "\begindata" should be ignored,
            even if it contains "\begindata", as long as it is not on an isolated line.

            So, in other words, this is still text.

            DELTA_T_A       =   32.184
            K               =    1.657D-3
            EB              =    1.671D-2
            M               = (  6.239996D0   1.99096871D-7 )

                    \begindata

                    FRAME_VG2_CONE_CLOCK     = -32200
                    FRAME_-32200_NAME        = 'VG2_CONE_CLOCK'
                    FRAME_-32200_CLASS       = 4
                    BEGINTEXT = ('Here''s some text containing +',
                                 '\begintext'
                                )

            \begintext

                    IGNORED = 7

            """

        d = from_text(text, commented=True)
        self.assertIn('FRAME_VG2_CONE_CLOCK', d)
        self.assertEqual(d['BEGINTEXT'], ['Here\'s some text containing +',
                                          r'\begintext'])
        self.assertNotIn('DELTA_T_A', d)
        self.assertNotIn('IGNORED', d)
        self.assertEqual(d['FRAME_-32200_NAME'], 'VG2_CONE_CLOCK')

        self.assertRaises(ParseException, from_text, text, commented=False)


#########################################################################################
# Perform unit testing if executed from the command line
#########################################################################################

if __name__ == '__main__':
    unittest.main()

#########################################################################################
