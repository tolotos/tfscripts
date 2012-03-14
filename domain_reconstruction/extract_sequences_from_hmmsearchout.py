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

#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc = '''%prog takes pickled clusters and stores all sequences as fasta from all
clusters for one network and species eg bzip and hsap.'''
cloptions = OptionParser(usage=usage, description=desc)
cloptions.add_option('-i', '--input', dest='input',
    help='Hmmsearch output filename', metavar='FILE')
cloptions.add_option('-f', '--fasta', dest='fasta',
    help='Fasta file', metavar='FILE')
(options, args) = cloptions.parse_args()
#==============================================================================


def read_hmmsearch_gi(source):
        GI = []

        try:
            #basename = os.path.basename(source)

            with open(source, "r") as file:
                for line in file.readlines():
                    if not line.startswith("#"):
                        line = line.rstrip().split()
                        GI.append(line[0])
                return GI
        except IOError:
            print "!----ERROR----!"
            print "File %s does not exit!" % source
            sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)


def return_entries_by_gi(source, gi_list):
        SG = {}

        try:
            #basename = os.path.basename(source)

            with open(source, "r") as file:
                for line in file:
                    if line.startswith(">"):
                        line = line.rstrip().split()
                        GI = line[0][1:]
                        if GI in gi_list:
                            SG[GI] = ""
                    else:
                        if GI in SG:
                            SG[GI] += line.rstrip()
                return SG
        except IOError:
            print "!----ERROR----!"
            print "File %s does not exit!" % source
            sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)



# GI = read_hmmsearch_gi(options.input)
# SG = return_entries_by_gi(options.fasta, GI)
# for gi in SG:
#     print gi
#     print SG[gi]
