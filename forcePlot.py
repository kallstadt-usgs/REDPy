# REDPy - Repeating Earthquake Detector in Python
# Copyright (C) 2016-2020  Alicia Hotovec-Ellis (ahotovec-ellis@usgs.gov)
# Licensed under GNU GPLv3 (see LICENSE.txt)

import redpy.config
import redpy.table
import redpy.plotting
import argparse
import numpy as np
import os

"""
Run this script to force plotting. Can be used after killing mid-run or updating settings.

usage: forcePlot.py [-h] [-v] [-a] [-c CONFIGFILE]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase written print statements
  -a, --all             replot everything, not just updated families
  -c CONFIGFILE, --configfile CONFIGFILE
                        use configuration file named CONFIGFILE instead of
                        default settings.cfg
"""

parser = argparse.ArgumentParser(description=
    "Run this script to force plotting. Can be used after killing mid-run or updating settings.")
parser.add_argument("-v", "--verbose", action="count", default=0,
    help="increase written print statements")
parser.add_argument("-a", "--all", action="count", default=0,
    help="replot everything, not just updated families")
parser.add_argument("-c", "--configfile",
    help="use configuration file named CONFIGFILE instead of default settings.cfg")
args = parser.parse_args()

if args.configfile:
    opt = redpy.config.Options(args.configfile)
    if args.verbose: print("Using config file: {0}".format(args.configfile))
else:
    opt = redpy.config.Options("settings.cfg")
    if args.verbose: print("Using config file: settings.cfg")

if args.verbose: print("Opening hdf5 table: {0}".format(opt.filename))
h5file, rtable, otable, ttable, ctable, jtable, dtable, ftable = redpy.table.openTable(opt)

if args.all:
    if args.verbose: print("Resetting plotting column...")
    ftable.cols.printme[0:ftable.attrs.nClust] = np.ones((ftable.attrs.nClust,))

if args.verbose: print("Creating plots...")
redpy.plotting.createPlots(rtable, ftable, ttable, ctable, otable, opt)

if args.verbose: print("Closing table...")
h5file.close()
if args.verbose: print("Done")