#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Jul 10, 2020 at 02:17 AM +0800

from urllib.request import urlretrieve
from argparse import ArgumentParser
from pathlib import Path

from yaml import safe_load


PWD = Path.resolve(Path(__file__).parent)
OUTPUT_DB = PWD / 'dec_db.yml'
DEC_GITLAB_URL = 'https://gitlab.cern.ch/lhcb-datapkg/Gen/DecFiles/-/raw/{}/dkfiles/{}.dec?inline=false'


def parse_input():
    parser = ArgumentParser(description='Download .dec files from CERN gitlab.')

    parser.add_argument('-d', '--dec-files',
                        nargs='+',
                        required=True,
                        help='''
specify the Event ID of .dec files to download
    ''')

    parser.add_argument('-o', '--output',
                        default='.',
                        help='''
specify output directory.
    ''')

    parser.add_argument('-t', '--tag',
                        default='v30r46',
                        help='''
specify DecFiles tag.
''')

    return parser.parse_args()


def dec_url_fmt(tag, file_path, url=DEC_GITLAB_URL):
    return url.format(tag, file_path)


if __name__ == '__main__':
    with open(OUTPUT_DB, 'r') as f:
        dk_file_db = safe_load(f)

    args = parse_input()

    dk_to_down = []
    for eid in args.dec_files:
        try:
            dk_to_down.append((eid, dk_file_db[eid]['RelativePath']))
        except KeyError:
            print('Unknown Event ID: {}.'.format(eid))

    for filename, rel_path in dk_to_down:
        try:
            url = dec_url_fmt(args.tag, rel_path)
            urlretrieve(url, args.output+'/'+filename)
        except Exception as err:
            print('Download of Event ID {} failed with error {}.'.format(
                filename, err.__class__.__name__
            ))
            print('The URL is: {}.'.format(url))
