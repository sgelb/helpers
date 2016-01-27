#!/usr/bin/env python3
'''output installed arch packages sorted by installed time or size'''

import sys
from pycman.config import init_with_config
import argparse
from datetime import datetime

pac = init_with_config("/etc/pacman.conf")


def get_data():
    items = []
    for p in sorted(pac.get_localdb().pkgcache, key=eval(args.sort),
                    reverse=args.re):
        items.append([p.name, datetime.fromtimestamp(
            int(p.installdate)).strftime('%d.%m.%Y'), convert_size(p.isize)])
    return items


def convert_size(size):
    for suffix in ['KB', 'MB', 'GB']:
        size /= 1024
        if size < 1024:
            return '{0:.1f} {1}'.format(size, suffix)

parser = argparse.ArgumentParser()
parser.add_argument("-t", action="store_const",
                    const="lambda x: x.installdate",
                    dest="sort", help="sort by install time")
parser.add_argument("-s", action="store_const",
                    const="lambda x: x.isize",
                    dest="sort", help="sort by install size")
parser.add_argument("-r", action="store_true", dest="re", default=False,
                    help="reverse output")
args = parser.parse_args()

if args.sort:
    items = get_data()
else:
    parser.print_help()
    sys.exit()

maxNameLength = max([len(i[0]) for i in items])
for i in items:
    print(str.ljust(i[0], maxNameLength), str.ljust(i[1], 11),
          str.rjust(i[2], 10))
