#!/usr/bin/env python3
'''output installed arch packages sorted by installed time or size'''

import sys
from pycman.config import init_with_config
from time import strftime
from optparse import OptionParser, OptionGroup
from datetime import datetime

h = init_with_config("/etc/pacman.conf")

def get_data():
    items = []
    for p in sorted(h.get_localdb().pkgcache, key=eval(options.sort), reverse=options.re):
        items.append([p.name, datetime.fromtimestamp(int(p.installdate)).strftime('%d.%m.%Y'),
                convert_size(p.isize)])
    return items

def convert_size(size):
    for suffix in ['KB', 'MB', 'GB']:
        size /= 1024
        if size < 1024:
            return '{0:.1f} {1}'.format(size, suffix)


usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)

parser.add_option("-t", action="store_const", const="lambda x: x.installdate", dest="sort",
        help="sort by install time")
parser.add_option("-s", action="store_const", const="lambda x: x.isize", dest="sort",
        help="sort by install size")
parser.add_option("-r", action="store_true", dest="re", default=False,
        help="reverse output")
(options, args) = parser.parse_args()

if options.sort:
    items = get_data()
else:
    parser.print_help()
    sys.exit()

max_col = max([len(i[0]) for i in items])

for i in items:
    print(str.ljust(i[0], max_col), str.ljust(i[1], 11), str.rjust(i[2], 10))
