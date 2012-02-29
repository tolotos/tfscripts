#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       extract_domainseqs_from_proteins.py
#
#==============================================================================
#Locate the Tfsuite module in ../
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '../../'))
#==============================================================================
from optparse import OptionParser
from ete2 import Tree
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc = '''%prog takes a tree in newick format and converts the species names
          in format species_name (eg. Gallus_gallus) to four letter id (ggal)'''
cloptions = OptionParser(usage=usage, description=desc)
cloptions.add_option('-t', '--tree', dest='tree',
    help='Filename for the supplied phylogeny', metavar='FILE')
cloptions.add_option('-o', '--outfile', dest='outfile',
    help='Filename for the supplied phylogeny', metavar='FILE')
(options, args) = cloptions.parse_args()
#==============================================================================


def main():
    tree = Tree(options.tree, format=8)
    for leaf in tree.iter_leaves():
        if len(leaf.name.split("_")) == 2:
            name = leaf.name.split("_")
            short_name = str(name[0][0]) + str(name[1][:3])
            leaf.name = short_name.lower()
    tree.write(outfile=options.outfile, format=8)

if __name__ == '__main__':
    main()
