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
from Tfsuite.Parser.color import color
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes a filename and a list of colors and writes yaml file'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-y', '--yaml', dest = 'yaml',
    help = 'Filename for the yaml file', metavar='FILE',
    default = 'colors.yaml')
(options, args) = cloptions.parse_args()


color = Color()

Colors.rgb = {"red":[255,0,0]}

