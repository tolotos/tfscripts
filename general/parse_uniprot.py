#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       parse_uniprot.py
#
#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.uniprot import Uniprot
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes a list of uniprot ids and the uniprot database and returns
        the uniprot id plus all secondary accession ids.'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-u', '--uniprot', dest = 'uniprot_db',
    help = 'Uniprot database', metavar='FILE', default = '')
cloptions.add_option('-i', '--ids', dest = 'id_list',
    help = 'List of uniprot ids',
    metavar='FILE', default = '')
cloptions.add_option('-r', '--organism', dest = 'organism',
    help = 'The organism that should be extracted',
    metavar='FILE', default = '')
(options, args) = cloptions.parse_args()
#==============================================================================


uniprot = Uniprot()

uniprot.load(options.uniprot_db, options.organism)

ids = []
for line in open(options.id_list, "r").readlines():
    line = line.rstrip().split()
    for id in line:
        if id not in ids:
            ids.append(id)
        else:
            continue

for id in ids:
    for k,v in uniprot.ac.items():
        if id in v:
            print id
            print k,v
            print "---"
