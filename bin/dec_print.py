#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Jul 07, 2020 at 07:29 PM +0800

import sys

from decaylanguage import DecFileParser


def list_complement(l_m, l_s):
    return [i for i in l_m if i not in l_s]


if __name__ == '__main__':
    dec_file = sys.argv[1]

    parser = DecFileParser(dec_file)
    parser.parse()

    decays = list_complement(parser.list_decay_mother_names(),
                             parser.list_charge_conjugate_decays())

    for d in decays:
        print('Decay {}'.format(d))
        parser.print_decay_modes(d)
