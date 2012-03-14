#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       taxids_to_phylogeny.py
#
#==============================================================================
from optparse import OptionParser
from Itol import Itol
import sys
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc = '''%prog takes an input file containg ncbi taxids and sends them to 
          iTol and returns a phylogeny. If the ncbi taxonomy mapping is provided
          taxids are converted to scientifc names to process further.'''
cloptions = OptionParser(usage=usage, description=desc)
cloptions.add_option('-i', '--infile', dest='infile',
    help='File containg taxids',
    metavar='FILE', default='')
cloptions.add_option('-m', '--mapping', dest='mapping',
    help='NCBI taxid to scientific name mapping',
    metavar='FILE', default='0')
cloptions.add_option('-o', '--output', dest='output',
    help='basename for the output',
    metavar='FILE', default='')
(options, args) = cloptions.parse_args()
#==============================================================================


def query_itol(filename):
    itol = Itol()
    itol.set_upload_param('ncbiFile', filename)
    itol.set_upload_param('ncbiFormat', 'idsCollapsed')
    tree_id = itol.upload()
    print tree_id
    itol.set_export_param("tree", tree_id)
    itol.set_export_param("format", "newick")
    return itol.export()

print query_itol('/home/f_zimm01/ncbitest.txt')
