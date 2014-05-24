#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from optparse import OptionParser

from geometry import read



log = logging.getLogger('test_read')



def main(geo_path):
    geometry = read(geo_path)
    print geometry.render()



if __name__ == "__main__":
    log.addHandler(logging.StreamHandler())

    usage = """%prog GEO

GEO    Input .geo file."""

    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="count", dest="verbose",
                      help="Print verbose information for debugging.", default=0)
    parser.add_option("-q", "--quiet", action="count", dest="quiet",
                      help="Suppress warnings.", default=0)

    (options, args) = parser.parse_args()
    args = [arg.decode(sys.getfilesystemencoding()) for arg in args]

    log_level = (logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG,)[
        max(0, min(3, 1 + options.verbose - options.quiet))]

    log.setLevel(log_level)

    if not len(args) == 1:
        parser.print_usage()
        sys.exit(1)
        
    geo_path = args[0]

    main(geo_path)
