#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Jun 09, 2021 at 06:58 PM +0200

import sys
import operator

from particle.converters import PDG2EvtGenNameMap
from decaylanguage import DecFileParser
from itertools import zip_longest


def list_complement(l_m, l_s):
    return [i for i in l_m if i not in l_s]


class MyDecFileParser(DecFileParser):
    def print_decay_modes(self, mother,
                          pdg_name=False, print_model=True, ascending=False,
                          normalize=True):
        if pdg_name:
            mother = PDG2EvtGenNameMap[mother]

        dms = self._find_decay_modes(mother)

        ls_dict = dict()
        for dm in dms:
            bf, fsp_names, model, model_params = self._decay_mode_details(dm)
            model_params = [str(i) for i in model_params]
            ls_dict[bf] = (fsp_names, model, model_params)

        dec_details = list(ls_dict.values())
        ls_attrs_aligned = list(zip_longest(
            *[self._align_items(i) for i in zip(*dec_details)], fillvalue=''))

        ls = [(bf, ls_attrs_aligned[idx]) for idx, bf in enumerate(ls_dict)]
        ls.sort(key=operator.itemgetter(0), reverse=(not ascending))
        norm = sum([bf for bf, _ in ls]) if normalize else 1

        for bf, info in ls:
            if print_model:
                line = '  %.4f   %s     %s  %s' % (bf/norm, *info)
            else:
                line = '  %.4f   %s' % (bf/norm, info[0])
            print(line.rstrip()+';')

    def _decay_mode_details(self, decay_mode):
        bf, fsp_names, model, model_params = super()._decay_mode_details(
            decay_mode)

        # Don't omit the 'PHOTOS'!
        if list(decay_mode.find_data('photos')):
            model = 'PHOTOS ' + model

        return bf, fsp_names, model, model_params

    @staticmethod
    def _align_items(to_align, align_mode='left', sep=' '):
        """
        Left or right align all strings in a list to the same length.
        By default string is space-broke into sub-strings and each set of sub-
        string aligned individually.
        """
        if not isinstance(to_align[0], list):
            max_len = max(len(s) for s in to_align)
            if align_mode == 'left':
                return [s.ljust(max_len) for s in to_align]
            elif align_mode == 'right':
                return [s.rjust(max_len) for s in to_align]
            else:
                raise ValueError('Unknown align mode: {}'.format(align_mode))

        aligned = []
        for cat in zip_longest(*to_align, fillvalue=''):
            max_len = max(len(s) for s in cat)

            if align_mode == 'left':
                row = [s.ljust(max_len) for s in cat]
            elif align_mode == 'right':
                row = [s.ljust(max_len) for s in cat]
            else:
                raise ValueError('Unknown align mode: {}'.format(align_mode))

            aligned.append(row)

        return [sep.join(row) for row in zip(*aligned)]


if __name__ == '__main__':
    dec_file = sys.argv[1]

    parser = MyDecFileParser(dec_file)
    parser.parse()

    decays = list_complement(parser.list_decay_mother_names(),
                             parser.list_charge_conjugate_decays())

    for d in decays:
        print('Decay {}'.format(d))
        parser.print_decay_modes(d)
