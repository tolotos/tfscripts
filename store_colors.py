#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       store_colors.py
#
#==============================================================================
#Locate the Tfsuite module in ../
import sys, os
sys.path.append( os.path.join( os.getcwd(), '..' ) )
#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.color import Color
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes a filename and a list of colors and writes yaml file'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-y', '--yaml', dest = 'yaml',
    help = 'Filename for the color.yaml', metavar='FILE')
(options, args) = cloptions.parse_args()


color = Color()
color.load(options.yaml)
print color.random_rgb()
#color.store(options.yaml)
