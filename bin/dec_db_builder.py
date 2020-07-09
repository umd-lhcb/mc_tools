#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Jul 09, 2020 at 08:57 PM +0800

from re import search
from os import path
from glob import glob
from pathlib import Path

from yaml import dump
from chardet import detect  # This is needed because not all .dec files are encoded in UTF-8.


DEC_METADATA = [
    'EventType',
    'NickName',
    'Descriptor',
    'PhysicsWG',
    'Responsible',
    'Date',
]

PWD = path.abspath(path.dirname(__file__))
DKFILES = PWD + '/../dec_files/DecFiles/dkfiles/*.dec'
OUTPUT_DB = PWD + '/dec_db.yml'


def gen_match_from_meta(meta):
    return {m: r'^#\s?'+m+r': (.*)$' for m in meta}


def search_meta_in_line(line, meta_matcher):
    for meta, pattern in meta_matcher.items():
        result = search(pattern, line)
        if result:
            return meta, result.group(1).strip()  # Remove tailing whitespace

    return False, False


def search_meta_in_file(file_path, meta_matcher):
    meta_dict = {}

    with open(file_path) as f:
        for line in f:
            meta, val = search_meta_in_line(line, meta_matcher)
            if meta:
                meta_dict[meta] = val

    return file_path, meta_dict


def search_meta_in_bin(raw, meta_matcher, encoding):
    meta_dict = {}
    decoded = raw.decode(encoding).split('\n')

    for line in decoded:
        meta, val = search_meta_in_line(line, meta_matcher)
        if meta:
            meta_dict[meta] = val

    return meta_dict


def regulate_pathname(p):
    path = Path(p)
    filename, base_dir = path.stem, path.parent.stem
    return '{}/{}'.format(base_dir, filename)


if __name__ == '__main__':
    dk_file_db = {}
    meta_matcher = gen_match_from_meta(DEC_METADATA)

    for dk_file in glob(DKFILES):
        raw_data = open(dk_file, 'rb').read()
        encoding = detect(raw_data)['encoding']

        metadata = search_meta_in_bin(raw_data, meta_matcher, encoding)
        if metadata:
            file_path = regulate_pathname(dk_file)
            metadata['RelativePath'] = file_path
            dk_file_db[metadata['EventType']] = metadata

    with open(OUTPUT_DB, 'w') as f:
        dump(dk_file_db, f, default_flow_style=False)
