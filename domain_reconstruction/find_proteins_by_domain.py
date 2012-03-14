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
(options, args) = cloptions.parse_args()
#==============================================================================


def load_clustergroup(pickled_cg):
    '''Loads clusters from pickled objects.'''
    CG = pickle.load(open(pickled_cg, "r"))
    return CG


def main():
    CG = load_clustergroup(options.pickle)

    species = []
    for protein in CG.iter_proteins():
        if "PAS" in protein.arangement:
            # print ">%s_%s" % (protein.gene_name, protein.species)
            # print protein.seq
            species.append(protein.species)
    species = list(set(species))
    print species
if __name__ == '__main__':
    main()