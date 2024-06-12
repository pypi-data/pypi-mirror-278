#!/usr/bin/env python3
"""

fastDSD.py -- the main function to calculate DSD from input

DSD version 0.5, Copyright (C) 2013, Tufts University
@author -- Mengfei Cao, mcao01@cs.tufts.edu
161 College Ave., Medford, MA 02155, USA

This program is a free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA

 The program calculates DSD from input file and outputs DSD in
 specified format. If there are at most 3 nodes or the PPI network
 is too sparse (#edges/#nodes < 0.5), it won't work

usage: DSDmain.py [-h] [-n NRW] [-o OUTFILE] [-q] [-f] [-m {1,2,3}]
                  [--outformat {matrix,list,top}] [-k NTOP] [-t THRESHOLD]
                  infile

parses PPIs from infile and calculates DSD

positional arguments:
  infile                read PPIs from infile, either a .csv or .tab file that
                        contains a tab/comma/space delimited table with both
                        IDs at first row and first column, or a .list file
                        that contains for each line one interacting pair

optional arguments:
  -h, --help            show this help message and exit
  -c, --converge        calculate the converged DSD, ignore the length of
                        random walks
  -n NRW, --nRW NRW     length of random walks, 5 by default
  -o OUTFILE, --outfile OUTFILE
                        output DSD file name, tab delimited tables, stdout by
                        default
  -q, --quiet           turn off status message
  -f, --force           calculate DSD for the whole graph despite it is not
                        connected if it is turned on; otherwise, calculate DSD
                        for the largest component
  -m {1,2,3}, --outFMT {1,2,3}
                        the format of output DSD file: type 1 for matrix; type
                        2 for pairs at each line; type 3 for top K proteins
                        with lowest DSD. Type 1 by default
  --outformat {matrix,list,top}
                        the format of output DSD file: 'matrix' for matrix,
                        type 1; 'list' for pairs at each line, type 2; 'top'
                        for top K proteins with lowest DSD, type 3. 'matrix'
                        by default
  -k NTOP, --nTop NTOP  if chosen to output lowest DSD nodes, output at most K
                        nodes with lowest DSD, 10 by default
  -t THRESHOLD, --threshold THRESHOLD
                        threshold for PPIs' confidence score, if applied


Note: *when -f is turned on, any DSDs w.r.t. nodes with 0 degree will be
      invalid: entries in DSD matrix will be output as NA

      *when the largest connected component(LCC) is extracted, we only
      calculate pairwise DSDs between nodes in LCC; the output will
      also only cover those in LCC; for "list" output, if either node is
      not in LCC, the DSD entry will be "NotConnected"

"""

INFILE = "/afs/csail/u/s/samsl/db/Coral/Pdam/candidate_pairs_mwt100_asof_20200617_50_800.out.positive"


import sys
import numpy as np
import networkx as nx
import argparse
from . import dsdcore
from . import dsdio

def main():
    temp = "parses PPIs from infile and calculates DSD"
    parser = argparse.ArgumentParser(description=temp)

    parser.add_argument("infile", help="read PPIs from tab-delimited edge list (with optional weights)")
    parser.add_argument("--converge",
                        default=False, help="calculate converged DSD",
                        action="store_true")
    parser.add_argument("-n", "--nRW", default=5, help="length of random walks, 5 by default", type=int)
    parser.add_argument("-w", "--ppip", help="directory containing PPI pathway files")
    parser.add_argument("-r", "--pathprob", default = "0.7", help="probability of remaining on a path given that you are already on it")
    parser.add_argument("-o", "--outfile", help="output DSD file name, tab delimited tables, stdout by default")
    parser.add_argument("-q", "--quiet", default=False, help="turn off status message", action="store_true")
    parser.add_argument("-f", "--force", default=False, help="calculate DSD for the whole graph despite it is not connected if it is turned on; otherwise, calculate DSD for the largest component ", action="store_true")
    parser.add_argument("-m", "--outFMT", default="1",
                        help="the format of output DSD file: type 1 for matrix; type 2 for pairs at each line; type 3 for top K proteins with lowest DSD. Type 1 by default", type=int, choices=[1, 2, 3])
    parser.add_argument("--outformat", default="matrix",
                        help="the format of output DSD file: 'matrix' for matrix, type 1; 'list' for pairs at each line, type 2; 'top' for top K proteins with lowest DSD, type 3. 'matrix' by default", choices=['matrix', 'list', 'top'])
    parser.add_argument("-k", "--nTop", default=10, help="if chosen to output lowest DSD nodes, output at most K nodes with lowest DSD, 10 by default", type=int)
    parser.add_argument("-t", "--threshold", help="threshold for PPIs' confidence score, if applied", type=float, default=0.5)
    parser.add_argument("-c", "--confidence", help="use information about interaction confidence (cDSD)",action="store_true")
    parser.add_argument("-a", "--augment", help="augment with high-confidence signaling pathway data (caDSD: requires -c)",action="store_true")
    parser.add_argument("-p", "--properties", help="make use of topological properties of signaling pathways (capDSD: requireds -ca)",action="store_true")

    options = parser.parse_args()

    sStar = '********************************************************'

    if options.outformat is not None:
        if options.outformat == "matrix":
            options.outFMT = 1
        elif options.outformat == "list":
            options.outFMT = 2
        elif options.outformat == "top":
            options.outFMT = 3

    if options.converge:
        options.nRW = -1
    else:
        if options.nRW < 0:
            print('THE LENGTH OF RANDOM WALKS SPECIFIED IS NOT VALID!',file=sys.stderr)

    # DSD type
    dsdType = ""
    if options.confidence:
        dsdType += "c"
    if options.augment:
        if "c" in dsdType:
            dsdType += "a"
        else:
            print(sStar,file=sys.stderr)
            print("-a requires -c",file=sys.stderr)
            print(sStar,file=sys.stderr)
            sys.exit(1)
    if options.properties:
        if "ca" in dsdType:
            dsdType += "p"
        else:
            print(sStar,file=sys.stderr)
            print("-p requires -ca",file=sys.stderr)
            print(sStar,file=sys.stderr)
            sys.exit(1)
    dsdType += "DSD"

    if not options.quiet:
        print(sStar)
        print('Start parsing PPI file: ', options.infile)
        if options.converge:
            print(f'calculate the converged {dsdType}')
        else:
            print(f'the length of random walks used to calculate {dsdType} is {options.nRW}')
        temp = 'the output format is chosen as No.' + str(options.outFMT)
        if options.outFMT == 1:
            print(temp, ":\n        (DSD matrix)")
            if options.outfile is not None:
                options.outfile = options.outfile + '.DSD1'
        elif options.outFMT == 2:
            print(temp, ":\n        (interacting pair list)")
            if options.outfile is not None:
                options.outfile = options.outfile + '.DSD2'
        elif options.outFMT == 3:
            print(temp, ":\n        (top K nodes with lowest DSD)")
            if options.outfile is not None:
                options.outfile = options.outfile + '.DSD3'
        if options.threshold is not None:
            print('the threshold for PPIs is specified as', options.threshold)
        else:
            options.threshold = -1
        print(sStar)

    ### Parse input file
    ### get the adjacency matrix and names of files
    if "c" in dsdType:
        G = nx.read_weighted_edgelist(options.infile)
        wG = nx.Graph()
        for (u,v,d) in G.edges.data():
            if d['weight'] >= options.threshold:
                wG.add_edge(u,v,weight=d['weight'])
        del G
        G = wG
    else:
        G = nx.read_edgelist(options.infile,data=False)

    if "a" in dsdType:
        raise NotImplementedError("Augment not yet implemented")

    if "p" in dsdType:
        raise NotImplementedError("Properties not yet implemented")

    N = len(G)
    M = len(G.edges)
    if not options.quiet:
        print(f'Done with parsing, there are {N} different nodes and {M} different PPIs originally')

    ### check graph connectivity
    cc = list(nx.connected_components(G))
    nc = len(cc)
    isConnected = len(cc) == 1

    if not isConnected and options.force:
        print(sStar,file=sys.stderr)
        print("!!!!!!! Warnning: the network is not connected, !!!!!!!!",file=sys.stderr)
        print("! calculating all pairs of DSD might not be meaningful !",file=sys.stderr)
        print(sStar,file=sys.stderr)
    if not isConnected and not options.force:
        print(sStar,file=sys.stderr)
        print("!!!!!!! Warnning: the network is not connected, !!!!!!!!",file=sys.stderr)
        print("****** calculate for the largest component instead *****",file=sys.stderr)
        print(sStar,file=sys.stderr)

        maxCCnodes = max(cc, key=lambda x: len(x))
        G = G.subgraph(maxCCnodes)
        N = len(G)
        M = len(G.edges)
        if not options.quiet:
            print(f"There are {nc} components and the largest connected component has {N} different nodes and {M} edges")

    if N < 3:
        print("Error: can't run DSD module on this PPI network, too small",file=sys.stderr)
        sys.exit(1)
    if M < N*0.5:
        print("Error: can't run DSD module on this PPI network, too sparse",file=sys.stderr)
        sys.exit(1)
    if not options.quiet:
        print('Building transition matrix...')

    names = list(G.nodes)
    DSD = dsdcore.calc_dsd(G, options.nRW, options.quiet)

    if options.outfile is not None:
        ofile = open(options.outfile, 'w')
    else:
        ofile = sys.stdout

    if not options.quiet:
        if options.outfile is not None:
            print('Finish calculating DSD, start writing into',options.outfile)
        else:
            print('Finish calculating DSD, start writing into stdout')

    if N <= options.nTop and options.outFMT == 3:
        options.nTop = N/2
        print(sStar,file=sys.stderr)
        print('Warning: The specified k is larger than the maximum number of nodes and thus is reset as {options.nTop} by default',file=sys.stderr)
        print(sStar,file=sys.stderr)

    if options.outFMT == 1:
        if dsdio.writeoutMatrix(DSD, names, ofile):
            if not options.quiet:
                print("The DSD matrix is written!")
        else:
            print("Can't write DSD into file!",file=sys.stderr)

    if options.outFMT == 2:
        if dsdio.writeoutList(DSD, names, options.infile, ofile):
            if not options.quiet:
                print('The DSD values between interacting nodes are written!')
        else:
            print("Can't write DSD into file!",file=sys.stderr)

    if options.outFMT == 3:
        if dsdio.writeoutToplist(DSD, names, ofile, options.nTop):
            if not options.quiet:
                print('The DSD values between nodes and those with top k lowest DSDs each row are written!')
        else:
            print("Can't write DSD into file!",file=sys.stderr)

    ofile.close()
