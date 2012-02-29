#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#  store_clusters_simple.py
#==============================================================================
#Locate the Tfsuite module in ../
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '../../'))
#==============================================================================
from optparse import OptionParser
from Tfsuite.core.clustergroup import ClusterGroup
import cPickle as pickle
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc = '''%prog takes orthomcl or proteinortho output (clusters) and creates
          a pickable clustergroup object. In addition a fasta, xdom, arrangements
          families and biomart mapping file are beeing attached.'''
cloptions = OptionParser(usage=usage, description=desc)
cloptions.add_option('-c', '--clusters', dest='clusters',
    help='Clusters', metavar='FILE',
    default='')
cloptions.add_option('-f', '--fasta', dest='fasta',
    help='Fasta file containing sequences of Proteins', metavar='FILE',
    default='')
cloptions.add_option('-d', '--domains', dest='dom_arang',
    help='Domain arrangements', metavar='FILE',
    default='')
cloptions.add_option('-m', '--familymapping', dest='family',
    help='Mapping from domain arrangement to family.', metavar='FILE',
    default='')
cloptions.add_option('-b', '--biomart', dest='biomart',
    help='Mapping from gene_name to uniprot and associated name.', metavar='FILE',
    default='')
cloptions.add_option('-x', '--xdom', dest='xdom',
    help='xdom.', metavar='FILE',
    default='')
cloptions.add_option('-p', '--pickle', dest='pickle',
    help='Filename for the pickled clusters', metavar='FILE',
    default='clustergroup.p')
(options, args) = cloptions.parse_args()
#==============================================================================


def main():
    CG = ClusterGroup(options.clusters, "ProteinOrtho", name="CG1")
    CG.attach_sequences(options.fasta, "fasta")
    CG.attach_domains(options.xdom, "xdom")
    CG.attach_arangement(options.dom_arang, "arag")
    CG.attach_families(options.family, "fam")
    CG.attach_biomart(options.biomart, "biomart")
    pickle.dump(CG, open(options.pickle, "wb"))
if __name__ == '__main__':
    main()
