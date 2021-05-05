#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu May 06, 2021 at 01:55 AM +0200

from urllib.request import urlretrieve
from argparse import ArgumentParser
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from yaml import safe_load


PWD = Path.resolve(Path(__file__).parent)
OUTPUT_DB = PWD / '..' / 'dec_db.yml'
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

    parser.add_argument('-s', '--silent',
                        action='store_true',
                        help='''
suppresses output printouts.
''')

    parser.add_argument('-D', '--debug',
                        action='store_true',
                        help='''
turn on debug messages.
''')

    return parser.parse_args()


def rm_none(lst):
    return [i for i in lst if i is not None]


def dec_url_fmt(tag, file_path, url=DEC_GITLAB_URL):
    return url.format(tag, file_path)


def prep_params_for_download(eid, db, output_dir, tag, silent, debug):
    try:
        return eid, db[eid]['Filename'], output_dir, tag, silent, debug
    except KeyError:
        print('Unknown Event ID: {}.'.format(eid))


def download_dec(eid, filename, output_dir, tag, silent=False, debug=False):
    output_filename = eid + '--' + filename + '.dec'
    output_filename = output_filename.replace(',', '-').replace('=', '__')
    url = dec_url_fmt(tag, filename)

    try:
        urlretrieve(url, output_dir+'/'+output_filename)
        if debug:
            debug_msg = 'MC ID: {}\n'.format(eid)
            debug_msg += 'URL: {}\n'.format(url)
            return debug_msg
        if not silent and not debug:
            return ' open '+output_filename
    except Exception as err:
        err_msg = 'Download of Event ID {} failed with error {}.\n'.format(
            filename, err.__class__.__name__)
        err_msg += 'The URL is: {}.'.format(url)
        return err_msg


if __name__ == '__main__':
    with open(OUTPUT_DB, 'r') as f:
        dk_file_db = safe_load(f)

    args = parse_input()

    dk_to_down = [prep_params_for_download(
        eid, dk_file_db, args.output_dir, args.tag, args.silent, args.debug)
        for eid in args.dec_files]
    dk_to_down = rm_none(dk_to_down)

    with ThreadPoolExecutor() as exe:
        exec_results = [exe.submit(lambda p: download_dec(*p), params)
                        for params in dk_to_down]
        msg = [f.result() for f in exec_results]

    print('\n'.join(rm_none(msg)))
