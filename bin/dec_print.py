#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Jul 08, 2020 at 01:21 AM +0800

import sys
import operator

from particle.converters import PDG2EvtGenNameMap
from decaylanguage import DecFileParser


def list_complement(l_m, l_s):
    return [i for i in l_m if i not in l_s]


class MyDecFileParser(DecFileParser):
    def print_decay_modes(self, mother,
                          pdg_name=False, ascending=False):
        if pdg_name:
            mother = PDG2EvtGenNameMap[mother]

        dms = self._find_decay_modes(mother)

        output_dms = list()
        for dm in dms:
            dm_details = self._decay_mode_details(dm)
            output_dms.append((dm_details[0], '%-50s %20s %s' %
                               ('  '.join(p for p in dm_details[1]), dm_details[2], dm_details[3])))

        output_dms.sort(key=operator.itemgetter(0), reverse=(not ascending))
        norm = sum([bf for bf, _ in output_dms])

        for bf, info in output_dms:
            print('  %.4f : %s' % (bf/norm, info))  # Manuel wants the BF to be normalized and have 4 decimals.

    def _decay_mode_details(self, decay_mode):
        bf, fsp_names, model, model_params = super()._decay_mode_details(
            decay_mode)

        # Don't omit the 'PHOTOS'!
        if list(decay_mode.find_data('photos')):
            model = 'PHOTOS ' + model

        return bf, fsp_names, model, model_params


if __name__ == '__main__':
    dec_file = sys.argv[1]

    parser = MyDecFileParser(dec_file)
    parser.parse()

    decays = list_complement(parser.list_decay_mother_names(),
                             parser.list_charge_conjugate_decays())

    for d in decays:
        print('Decay {}'.format(d))
        parser.print_decay_modes(d)
