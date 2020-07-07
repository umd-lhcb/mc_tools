#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Jul 07, 2020 at 07:55 PM +0800

import sys
import operator

from particle.converters import PDG2EvtGenNameMap
from decaylanguage import DecFileParser
from decaylanguage.dec.dec import get_final_state_particle_names, \
    get_branching_fraction


def list_complement(l_m, l_s):
    return [i for i in l_m if i not in l_s]


class MyDecFileParser(DecFileParser):
    def print_decay_modes(self, mother,
                          pdg_name=False, print_model=True, ascending=False):
        if pdg_name:
            mother = PDG2EvtGenNameMap[mother]

        dms = self._find_decay_modes(mother)

        l = list()
        if print_model:
            for dm in dms:
                dm_details = self._decay_mode_details(dm)
                l.append((dm_details[0], '%-50s %15s %s' %
                          ('  '.join(p for p in dm_details[1]), dm_details[2], dm_details[3])))
        else:
            for dm in dms:
                fsp_names = get_final_state_particle_names(dm)
                l.append((get_branching_fraction(dm),
                         '%-50s' % ('  '.join(p for p in fsp_names))))

        l.sort(key=operator.itemgetter(0), reverse=(not ascending))

        for bf, info in l:
            print('  %.4f : %s' % (bf, info))  # Manuel wants the BF to have 4 decimals.


if __name__ == '__main__':
    dec_file = sys.argv[1]

    parser = MyDecFileParser(dec_file)
    parser.parse()

    decays = list_complement(parser.list_decay_mother_names(),
                             parser.list_charge_conjugate_decays())

    for d in decays:
        print('Decay {}'.format(d))
        parser.print_decay_modes(d)
