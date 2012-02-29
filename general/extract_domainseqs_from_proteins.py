#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       extract_domainseqs_from_proteins.py
#
#==============================================================================
#Locate the Tfsuite module in ../
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
#==============================================================================
from optparse import OptionParser
from Tfsuite.parser.cyto import Cyto
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
cloptions.add_option('-n', '--network', dest='net_in',
    help='Network input file', metavar='FILE', default='')
(options, args) = cloptions.parse_args()
#==============================================================================


def load_clustergroup(pickled_cg):
    '''Loads clusters from pickled objects.'''
    CG = pickle.load(open(pickled_cg, "r"))
    return CG


def load_network(file, name):
    network = Cyto()
    network.load(file)
    network.name = name
    return network


def main():
    CG = load_clustergroup(options.pickle)
    network = load_network(options.net_in, "HLH")

    for protein in CG.iter_proteins():
        if protein.species == "hsap" and protein.domains[0].id == "HLH":
            if protein.associated_name in network.nodes:
                print ">%s" % protein.associated_name
                for domain in protein.domains:
                    print protein.seq[domain.begin - 20:domain.end + 20]

if __name__ == '__main__':
    main()
