##########################################################################################
# textkernel/tests/test_from_file.py
##########################################################################################

import copy
import pathlib
import unittest
import sys

from textkernel import from_file, update_dict


class Test_from_file(unittest.TestCase):

    def test_from_file(self):

        # Parse every test file
        tkdicts = {}
        root_dir = pathlib.Path(sys.modules['textkernel'].__file__).parent.parent
        test_file_dir = root_dir / 'test_files'
        test_paths = test_file_dir.glob('*')
        for path in test_paths:
            tkdicts[path.name] = from_file(path)

        # An update fills in missing frame names
        # cas_status_v04.tf, cas_iss_v10.ti
        cas_status = copy.deepcopy(tkdicts['cas_status_v04.tf'])
        keys = list(cas_status['FRAME'].keys())
        self.assertEqual(keys,
                         [-82000, -82001, -82002, -82008, -82009, -82101, -82102, -82103,
                          -82104, -82105, -82106, -82107, -82108, -82350, -82351, -82360,
                          -82361, -82368, -82369, -82370, -82371, -82372, -82378, -82730,
                          -82731, -82732, -82733, -82734, -82740, -82760, -82761, -82762,
                          -82763, -82764, -82765, -82790, -82791, -82792, -82810, -82811,
                          -82812, -82813, -82814, -82820, -82821, -82822, -82840, -82842,
                          -82843, -82844, -82845, -82849, -82890, -82891, -82892, -82893,
                          -82898])
        self.assertEqual(cas_status['FRAME'][-82898],
                         {'BVT_STATUS': 'INELIGIBLE',
                          'INSTRUMENT_TYPE': 'RADIATOR',
                          'ID': -82898,
                          'CENTER': -82})

        tkdict = from_file(test_file_dir / 'cas_iss_v10.ti', tkdict=cas_status)
        self.assertIs(tkdict, cas_status)
        self.assertIs(tkdict['FRAME'][-82360], tkdict['FRAME']['CASSINI_ISS_NAC'])
        self.assertIs(tkdict['FRAME'][-82361], tkdict['FRAME']['CASSINI_ISS_WAC'])

        merged = update_dict(tkdicts['cas_status_v04.tf'],
                             copy.deepcopy(tkdicts['cas_iss_v10.ti']))
        self.assertEqual(merged, tkdict)

        # Multiple new body name keys inserted into a pre-existing sub-dictionary
        # new_horizons_295.tsc, nh_v110.tf
        nh_295 = copy.deepcopy(tkdicts['new_horizons_295.tsc'])
        body_keys = list(nh_295['BODY'].keys())
        self.assertEqual(body_keys, [-98, 'NEW HORIZONS'])
        self.assertIs(nh_295['BODY'][-98], nh_295['BODY']['NEW HORIZONS'])

        tkdict = from_file(test_file_dir / 'nh_v110.tf', tkdict=nh_295)
        self.assertIs(nh_295, tkdict)
        self.assertIs(nh_295['BODY'][-98], nh_295['BODY']['NEW_HORIZONS'])
        self.assertIs(nh_295['BODY'][-98], nh_295['BODY']['NH'])
        self.assertIs(nh_295['BODY'][-98], nh_295['BODY']['NH_SPACECRAFT'])

        merged = update_dict(tkdicts['new_horizons_295.tsc'],
                             copy.deepcopy(tkdicts['nh_v110.tf']))
        self.assertEqual(merged, tkdict)

        # Body name inferred from frame name
        # cas_rocks_v18.tf
        tkdict = tkdicts['cas_rocks_v18.tf']
        self.assertIn('BODY', tkdict)
        self.assertIs(tkdict['BODY'][619], tkdict['BODY']['YMIR'])
        self.assertEqual(tkdict['BODY'][619], {'ID': 619, 'NAME': 'YMIR'})
        self.assertIs(tkdict['FRAME'][619], tkdict['FRAME']['IAU_YMIR'])

        # TKFRAME_<name>_* identifications
        # earth_topo_050714.tf
        tkdict = tkdicts['earth_topo_050714.tf']
        self.assertIs(tkdict['TKFRAME']['DSS-12_TOPO'], tkdict['TKFRAME'][1399012])
        self.assertIs(tkdict['FRAME']['DSS-12_TOPO'], tkdict['FRAME'][1399012])

        self.assertIs(tkdict['BODY']['DSS-12'], tkdict['BODY'][399012])
        self.assertEqual(tkdict['BODY'][399012], {'ID': 399012, 'NAME': 'DSS-12'})

        # Order of merges shouldn't matter (except in TEXT_KERNEL_ID)
        answer = copy.deepcopy(tkdicts['cas_status_v04.tf'])
        answer = update_dict(answer, copy.deepcopy(tkdicts['cas_v40.tf']))
        answer = update_dict(answer, copy.deepcopy(tkdicts['cas_iss_v10.ti']))
        answer['TEXT_KERNEL_ID'] = set(answer['TEXT_KERNEL_ID'])

        keys = ['cas_status_v04.tf', 'cas_v40.tf', 'cas_iss_v10.ti']
        orders = [(0,1,2), (0,2,1), (1,0,2), (1,2,0), (2,0,1), (2,1,0)]

        for i,j,k in orders:
            test = from_file(test_file_dir / keys[i])
            test = from_file(test_file_dir / keys[j], tkdict=test)
            test = from_file(test_file_dir / keys[k], tkdict=test)
            test['TEXT_KERNEL_ID'] = set(test['TEXT_KERNEL_ID'])
            self.assertEqual(test, answer)

        # "INS" identifier checks
        # juno_jiram_v00.ti
        tkdict = tkdicts['juno_jiram_v00.ti']
        self.assertIs(tkdict['INS'][-61420], tkdict['INS']['JUNO_JIRAM_S'])
        self.assertIs(tkdict['FRAME'][-61420], tkdict['FRAME']['JUNO_JIRAM_S'])
        self.assertEqual(tkdict['FRAME'][-61420], {'ID': -61420,
                                                   'NAME': 'JUNO_JIRAM_S',
                                                   'CENTER': -61})
        self.assertNotIn(-61, tkdict['FRAME'])


##########################################################################################
# Perform unit testing if executed from the command line
##########################################################################################

if __name__ == '__main__':
    unittest.main()

##########################################################################################
