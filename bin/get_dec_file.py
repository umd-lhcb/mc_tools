#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri Jul 10, 2020 at 02:26 AM +0800

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

    parser.add_argument('-o', '--output-dir',
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


def download_dec(eid, filename, output_dir, tag):
    output_filename = eid + '-' + filename + '.dec'
    url = dec_url_fmt(tag, filename)

    try:
        urlretrieve(url, output_dir+'/'+output_filename)
    except Exception as err:
        err_msg = 'Download of Event ID {} failed with error {}.\n'.format(
            filename, err.__class__.__name__)
        err_msg += 'The URL is: {}.\n'.format(url)
        return err_msg


if __name__ == '__main__':
    with open(OUTPUT_DB, 'r') as f:
        dk_file_db = safe_load(f)

    args = parse_input()

    dk_to_down = []
    for eid in args.dec_files:
        try:
            dk_to_down.append((eid, dk_file_db[eid]['Filename']))
        except KeyError:
            print('Unknown Event ID: {}.'.format(eid))

    for eid, filename in dk_to_down:
        download_dec(eid, filename, args.output_dir, args.tag)
