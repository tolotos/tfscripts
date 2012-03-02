#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       correlate_cafe_count.py
#
#==============================================================================
#Locate the Tfsuite module in ../
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '../../'))
#==============================================================================
from optparse import OptionParser
from Tfsuite.core.network import Network
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc = '''%prog loads a network'''
cloptions = OptionParser(usage=usage, description=desc)
cloptions.add_option('-p', '--pickle', dest='pickle',
    help='Filename for the pickled clusters', metavar='FILE',
    default='pickled_orthomcl_clusters.p')
cloptions.add_option('-n', '--network', dest='net_in',
    help='Network input file', metavar='FILE', default='')
(options, args) = cloptions.parse_args()
#==============================================================================


def main():
    #clusters = load_clusters(options.pickle)
    NET = Network(options.net_in, "ppsimple", "NF")
    NET.connect_to_cytoscape("http://localhost:9000")
    NET.create_cytoscape_network()
    NET.scale_nodesize_by_connectivity(range(1, 50, 2))
if __name__ == '__main__':
    main()
