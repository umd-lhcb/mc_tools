#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Jul 09, 2020 at 07:40 PM +0800

from re import search


DEC_METADATA = [
    'EventType',
    'NickName',
    'Descriptor',
    'PhysicsWG',
    'Responsible',
    'Date',
]


def gen_match_from_meta(meta):
    return {m: r'^# '+m+r': (.*)$' for m in meta}


def search_meta_in_line(line, meta_matcher):
    for meta, pattern in meta_matcher.items():
        result = search(pattern, line)
        if result:
            return meta, result.group(1)

    return False, False


def search_meta_in_file(file_path, meta_matcher):
    meta_dict = {}

    with open(file_path) as f:
        for line in f:
            meta, val = search_meta_in_line(line, meta_matcher)
            if meta:
                meta_dict[meta] = val

    return file_path, meta_dict
