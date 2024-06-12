##########################################################################################
# textkernel/tests_name_grammar.py
##########################################################################################

import unittest

from pyparsing                import StringEnd
from textkernel._NAME_GRAMMAR import _NAME_GRAMMAR


class Test_NAME_GRAMMAR(unittest.TestCase):

    def test_NAME_GRAMMAR(self):
        p = _NAME_GRAMMAR + StringEnd()
        func = p.parse_string

        self.assertEqual(func('BODY610_GM')[0],             ('BODY', 610, 'GM'))
        self.assertEqual(func('CK_-61113_SCLK')[0],         ('CK', -61113, 'SCLK'))
        self.assertEqual(func('DELTET/DELTA_T_A')[0],       ['DELTET', 'DELTA_T_A'])
        self.assertEqual(func('FRAME-82731_TYPE')[0],       ('FRAME', -82731, 'TYPE'))
        self.assertEqual(func('FRAME_-82731TYPE')[0],       ('FRAME', -82731, 'TYPE'))
        self.assertEqual(func('INS-61411_FRAME')[0],        ('INS', -61411, 'FRAME'))
        self.assertEqual(func('INS-82360_F/NUMBER')[0],     ('INS', -82360, 'F/NUMBER'))
        self.assertEqual(func('KERNELS_TO_LOAD')[0],        'KERNELS_TO_LOAD')
        self.assertEqual(func('NAIF_BODY_CODE')[0],         'NAIF_BODY_CODE')
        self.assertEqual(func('OBJECT_399005_FRAME')[0],    ('OBJECT', 399005, 'FRAME'))
        self.assertEqual(func('SCLK_PART_END_82')[0],       ('SCLK', -82, 'PART_END'))
        self.assertEqual(func('SCLK01_TIME_SYS_98')[0],     ('SCLK', -98, '01_TIME_SYS'))
        self.assertEqual(func('TEXT_KERNEL_ID')[0],         'TEXT_KERNEL_ID')
        self.assertEqual(func('TKFRAME_-82008_SPEC')[0],    ('TKFRAME', -82008, 'SPEC'))
        self.assertEqual(func('TKFRAME_DSS-14_TOPO_Q')[0],  ('TKFRAME', 'DSS-14_TOPO',
                                                             'Q'))


##########################################################################################
# Perform unit testing if executed from the command line
##########################################################################################

if __name__ == '__main__':
    unittest.main()

##########################################################################################
