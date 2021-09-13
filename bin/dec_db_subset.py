#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Sep 13, 2021 at 03:20 PM +0200

import yaml

from argparse import ArgumentParser
from os.path import abspath, dirname, join


def parse_input():
    parser = ArgumentParser('save a subset of .dec file YAML DB.')

    parser.add_argument('output', help='specify output YAML DB.')

    parser.add_argument('mc_id', nargs='+', action='extend',
                        help='specify MC IDs.')

    parser.add_argument('--db', default=join(
        abspath(dirname(__file__)), '../dec_db.yml'),
        help='specify YAML DB path.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()

    with open(args.db) as f:
        db = yaml.safe_load(f)

    db_subset = {k: db[k] for k in args.mc_id if k in db}

    with open(args.output, 'w') as f:
        f.write(yaml.dump(db_subset))
