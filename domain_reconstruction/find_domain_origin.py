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
import cPickle as pickle
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc = '''%prog takes pickled clusters and stores all sequences as fasta from all
clusters for one network and species eg bzip and hsap.'''
cloptions = OptionParser(usage=usage, description=desc)
cloptions.add_option('-p', '--pickle', dest='pickle',
    help='Filename for the pickled clusters', metavar='FILE',
    default='pickled_orthomcl_clusters.p')
cloptions.add_option('-t', '--tree', dest='tree',
    help='Filename for the supplied phylogeny', metavar='FILE')
(options, args) = cloptions.parse_args()
#==============================================================================


def load_clustergroup(pickled_cg):
    '''Loads clusters from pickled objects.'''
    CG = pickle.load(open(pickled_cg, "r"))
    return CG


def main():
    CG = load_clustergroup(options.pickle)
    t = Tree(options.tree, format=8)
    species = []
    arag = []
    for protein in CG.iter_proteins():
        if "PAS" in protein.arangement: #and "HLH" in protein.arangement:
            print ">%s_%s" % (protein.gene_name, protein.species)
            # print protein.seq
            print protein.arangement
            arag.append(",".join(protein.arangement))
            species.append(protein.species)
    arag = list(set(arag))
    print arag
    species = list(set(species))
    mrca = t.get_common_ancestor(species)
    print mrca.name
    print species
if __name__ == '__main__':
    main()
