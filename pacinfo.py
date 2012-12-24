#!/usr/bin/env python3
'''output installed arch packages sorted by installed time or size'''

import sys
from pycman.config import init_with_config
from time import strftime
from optparse import OptionParser, OptionGroup
from datetime import datetime

h = init_with_config("/etc/pacman.conf")

def by_time():
    items = []
    for p in sorted(h.get_localdb().pkgcache, key=lambda x: x.installdate, reverse=options.re):
        items.append([p.name, datetime.fromtimestamp(int(p.installdate)).strftime('%d.%m.%Y')])
    return items

def by_size():
    items = []
    for p in sorted(h.get_localdb().pkgcache, key=lambda x: x.isize, reverse=options.re):
        items.append([p.name, convert_size(p.isize)])
    return items

def convert_size(size):
    for suffix in ['KB', 'MB', 'GB']:
        size /= 1024
        if size < 1024:
            return '{0:.1f} {1}'.format(size, suffix)


usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)

parser.add_option("-t", action="store_true", dest="time",
        help="sort by install time")
parser.add_option("-s", action="store_true", dest="size",
        help="sort by install size")
parser.add_option("-r", action="store_true", dest="re", default=False,
        help="reverse output")
(options, args) = parser.parse_args()

if options.time:
    items = by_time()
elif options.size:
    items = by_size()
else:
    parser.print_help()
    sys.exit()

max_col = max([len(i[0]) for i in items])

for i in items:
    print(str.ljust(i[0], max_col), str.rjust(i[1], 10))
