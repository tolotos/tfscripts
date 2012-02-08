#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  store_orthomcl_clusters.py

#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.arangements import Arangements
from Tfsuite.Parser.fasta import read_fasta
from Tfsuite.Parser.biomart import Biomart
from Tfsuite.Parser.family import Family
from Tfsuite.Parser.proteinortho import ProteinOrtho
import os
import glob
import copy
import cPickle as pickle
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes orthomcl output (clusters) and creates a pickable object
        containing all loaded clusters.'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-c', '--clusters', dest = 'clusters',
    help = 'Clusters', metavar='FILE',
    default = '')
cloptions.add_option('-f', '--fasta', dest = 'fasta',
    help = 'Fasta file containing sequences of Proteins', metavar='FILE',
    default = '')
cloptions.add_option('-d', '--domains', dest = 'dom_arang',
    help = 'Domain arrangements', metavar='FILE',
    default = '')
cloptions.add_option('-m', '--familymapping', dest = 'family',
    help = 'Mapping from domain arrangement to family.', metavar='FILE',
    default = '')
cloptions.add_option('-b', '--biomart', dest = 'biomart',
    help = 'Mapping from gene_name to uniprot and associated name.', metavar='FILE',
    default = '')
cloptions.add_option('-p', '--pickle', dest = 'pickle',
    help = 'Filename for the pickled clusters', metavar='FILE',
    default = 'pickled_orthomcl_clusters.p')
(options, args) = cloptions.parse_args()
#==============================================================================
def create_clusters(f_clusters,f_arag,fasta_file,f_family, f_biomart):
    ''' Loads an orthomcl output file, to create clusters. In addition proteins
        are added from the corresponding hmmout file, species information is
        added from speciesMapping(Andreas) and fasta sequences for each protein
        are loaded. Function returns an interable with cluster objects'''
    proteinortho, arangements = ProteinOrtho(), Arangements() 
    family, biomart = Family(), Biomart()
    proteinortho.load(f_clusters)
    arangements.load(f_arag)
    family.load(f_family)
    biomart.load(f_biomart)




    for protein in arangements:
        protein.add_sequence(fasta_file,"fasta")
        
        protein.add_family(family)
        protein.add_identifiers(biomart)
    for cluster in proteinortho:
        cluster.add_proteins(arangements)
        cluster.add_cluster_to_members()
        cluster.add_family()
    return proteinortho

def main():
    clusters = create_clusters(options.clusters,
                               options.dom_arang,
                               options.fasta,
                               options.family,
                               options.biomart)
    pickle.dump(clusters, open(options.pickle, "wb"))
if __name__ == '__main__':
    main()

