#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       extract_domainseqs_from_proteins.py
#
#==============================================================================
#Locate the Tfsuite module in ../
import sys, os
sys.path.append( os.path.join( os.getcwd(), '..' ) )
#==============================================================================
from optparse import OptionParser
from Tfsuite.Classes.cluster import Cluster
from Tfsuite.Parser.cyto import Cyto
import cPickle as pickle
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes pickled clusters and stores all sequences as fasta from all
clusters for one network and species eg bzip and hsap.'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-p', '--pickle', dest = 'pickle',
    help = 'Filename for the pickled clusters', metavar='FILE',
    default = 'pickled_orthomcl_clusters.p')
cloptions.add_option('-n', '--network', dest = 'net_in',
    help = 'Network input file', metavar='FILE', default = '')
cloptions.add_option('-x', '--xdom', dest = 'xdom_in',
    help = 'Network input file', metavar='FILE', default = '')
(options, args) = cloptions.parse_args()
#==============================================================================

def load_clusters(clusters):
    '''Loads clusters from pickled objects.'''
    clusters = pickle.load(open(clusters,"r"))
    return clusters

def proteins_by_species(clusters,species):
    proteins = []
    for cluster in clusters:
        for member in cluster.members:
            if member.species == species:
                proteins.append(member)
    return proteins

def load_network(file,name):
    network = Cyto()
    network.load(file)
    network.name = name
    return network

def load_xdom(xdom):
    prots = {}
    with open(xdom,"r") as xdom:
        for line in xdom.readlines():
            line = line.rstrip().split()
            if len(line) > 0:
                if line[0].startswith(">"):
                    gene_name = line[0].split("|")[1]
                    prots[gene_name] = []
                else:
                    prots[gene_name].append(",".join(line[0:3]))
    return prots
xdom = load_xdom(options.xdom_in)

clusters = load_clusters(options.pickle)
network = load_network(options.net_in,"HLH")
proteins = proteins_by_species(clusters,"hsap")

for protein in proteins:
    if protein.associated_name in network.nodes.keys():
        print ">"+protein.associated_name
        for domain in xdom[protein.gene_name]:
            domain = domain.split(",")
            if domain[2] == "HLH":
                print protein.seq[int(domain[0]):int(domain[1])]
                    