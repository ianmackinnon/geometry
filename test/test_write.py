#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from optparse import OptionParser

from geometry import Geometry



log = logging.getLogger('test_write')



def main():
    geometry = Geometry()

    values = (-0.5, 0.0, 0.5)
    for z in values:
        for x in values:
            geometry.add_point(x, 0, z)

    geometry.add_prim((0, 1, 4, 3))
    geometry.add_prim((1, 2, 5, 4))
    geometry.add_prim((3, 4, 7, 6))
    geometry.add_prim((4, 5, 8, 7))

    for i, point in enumerate(geometry.points):
        geometry.set_point_attr_int("pointInt1", i, i)
        geometry.set_point_attr_float("pointFloat1", i, i * 0.1)
        geometry.set_point_attr_float("pointFloat3", i,
                                      [i * 1.1, i * 2.2, i * 3.3])
        geometry.set_point_attr_string("pointString1", i,
                                       """pointString1 value is %d \ " '""" % i)
        geometry.set_point_attr_float("pointFloat1", i, i * 0.1)

    for i, point in enumerate(geometry.prims):
        geometry.set_prim_attr_int("primInt1", i, i)
        geometry.set_prim_attr_float("primFloat1", i, i * 0.1)
        geometry.set_prim_attr_float("primFloat3", i,
                                      [i * 1.1, i * 2.2, i * 3.3])
        geometry.set_prim_attr_string("primString1", i,
                                       """primString1 value is %d \ " '""" % i)

    print geometry.render()


if __name__ == "__main__":
    log.addHandler(logging.StreamHandler())

    usage = """%prog"""

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

    if not len(args) == 0:
        parser.print_usage()
        sys.exit(1)

    main()
