#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Jun 09, 2021 at 07:19 PM +0200

from argparse import ArgumentParser
from decaylanguage import DecFileParser


def parse_input():
    parser = ArgumentParser(description='print out .dec file, prettified.')

    parser.add_argument('dec', help='path to .dec file.')

    parser.add_argument('-p', '--no-photos', action='store_false',
                        help="don't print PHOTOS.")
    parser.add_argument('-m', '--no-model', action='store_false',
                        help="don't print decay model.")

    return parser.parse_args()


def list_complement(l_m, l_s):
    return [i for i in l_m if i not in l_s]


if __name__ == '__main__':
    args = parse_input()

    parser = DecFileParser(args.dec)
    parser.parse()

    decays = list_complement(parser.list_decay_mother_names(),
                             parser.list_charge_conjugate_decays())

    for d in decays:
        print('Decay {}'.format(d))
        parser.print_decay_modes(
            d, keep_photos=args.no_photos, print_model=args.no_model)
