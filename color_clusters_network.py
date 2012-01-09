#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       correlate_cafe_count.py
#
#==============================================================================
from optparse import OptionParser
from Tfsuite.Classes.cluster import Cluster
from Tfsuite.Parser.cyto import Cyto
import cPickle as pickle
import xmlrpclib
import random
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog '''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-p', '--pickle', dest = 'pickle',
    help = 'Filename for the pickled clusters', metavar='FILE',
    default = 'pickled_orthomcl_clusters.p')
cloptions.add_option('-n', '--network', dest = 'net_in',
    help = 'Network input file', metavar='FILE', default = '')
(options, args) = cloptions.parse_args()
#==============================================================================


def load_clusters(clusters):
    '''Loads clusters from pickled objects.
       The count and cafe results are added to the pickled clusters and
       can then be processed further. (Analysis, new pickling.)'''
    clusters = pickle.load(open(clusters,"r"))
    return clusters

def load_network(net_file,name):
    server = connect_server("http://localhost:9000")
    cytoscape = server.Cytoscape
    title = name
    if cytoscape.hasCurrentNetwork() == True:
        old_id = cytoscape.getNetworkID()
        cytoscape.destroyNetwork(old_id)
        cytoscape.createNetwork(title)
    else:
        cytoscape.createNetwork(title)

    network = Cyto()
    network.load(net_file)

    return network, cytoscape

def connect_server(server_name):
    server = xmlrpclib.ServerProxy(server_name)
    return server

def color_by_cluster(id,cytoscape,cluster,color):
    red = color[0]
    green = color[1]
    blue = color[2]
    for member in cluster.members:
        if member.species == "hsap":
            for node in cytoscape.getNodes():
                if member.associated_name == str(node):
                    cytoscape.setNodeFillColor(id,[node], red,green,blue)

def color_by_arrangement(id, cytoscape, arag_dic,color):
    for arag, members in arag_dic.items():
        color = random_color(color)
        red = color[0]
        green = color[1]
        blue = color[2]
        print color, arag, members
        for member in members:
            for node in cytoscape.getNodes():
                if member == str(node):
                    cytoscape.setNodeFillColor(id,[node], red,green,blue)

def scale_nodesize_by_connectivity(range,id,cytoscape):
    size = 50
    for i in range:
        #print i
        for node in cytoscape.getNodes():
            #print node
            connections = len(cytoscape.getNodeNeighbors(id, node))
            #print connections
            #print "-----"
            if connections >= i:
                cytoscape.setNodeProperty(node,"Node Size", str(size))
        size +=6

def random_color(color):
        for i in range(len(color)):
            color[i] = random.randint(0,255)
        return color

def species_arangements(clusters,species):
    arag_dic = {}
    for cluster in clusters:
        for member in cluster.members:
            if member.species == species:
                arag = ",".join(member.domains)
                if arag in arag_dic:
                    arag_dic[arag].append(member.associated_name)
                else:
                    arag_dic[arag] = [member.associated_name]
    return arag_dic

def shape_by_arangement(arag_dic,id, cytoscape):
    shapes = ["trapezoid","rect_3d","round_rect","ellipse","triangle",
              "diamond","octagon","parallelogram","trapezoid_2",
              "rect","vee","hexagon"]
    if len(arag_dic) > len(shapes):
        print "Too many arangements, not enough shapes available!"
    else:
        for num, arangements in enumerate(arag_dic):
            for node in arag_dic[arangements]:
              #  print node,shapes[num], arangements
                cytoscape.setNodeProperty(node,"Node Shape", shapes[num])

def shape_by_cluster(id,cytoscape, clusters):
    shapes = ["trapezoid","rect_3d","round_rect","ellipse","triangle",
              "diamond","octagon","parallelogram","trapezoid_2",
              "rect","vee","hexagon"]
    if len(clusters.clusters) > len(shapes):
        print len(clusters.clusters)
        print "Too many clusters, not enough shapes available!"
    else:
        for num, cluster in enumerate(clusters):
            for member in cluster.members:
                cytoscape.setNodeProperty(member,"Node Shape", shapes[num])

def add_cluster_id_to_name(network,clusters, species, cytoscape):
        for cluster in clusters:
            id = "_CL"+cluster.name.split("_")[1]
            for member in cluster.members:
                if member.species == species:
                    for node in cytoscape.getNodes():
                        if member.associated_name == str(node):
                            cl_name = member.associated_name+id
                            cytoscape.setNodeProperty(node,"Node Label",cl_name)
        #for member in cluster:
         #   print member


def main():
    clusters = load_clusters(options.pickle)
    network = load_network(options.net_in,"HLH")
    network, cytoscape = network[0], network[1]
    nodes = network.nodes.keys()
    from_nodes, to_nodes = network.edges()
    cytoscape.createNodes(nodes)
    cytoscape.createEdges(from_nodes, to_nodes)
    #cytoscape.performDefaultLayout()
    cytoscape.performLayout("force-directed")
    id = cytoscape.getNetworkID()
    #shape_by_cluster(id,cytoscape,clusters)
    scale_nodesize_by_connectivity(range(1,50,2),id, cytoscape)
    arag_dic = species_arangements(clusters,"hsap")
    color = [0,0,0]
    color_by_arrangement(id,cytoscape,arag_dic,color)
    add_cluster_id_to_name(network,clusters,"hsap",cytoscape)

if __name__ == '__main__':
    main()
