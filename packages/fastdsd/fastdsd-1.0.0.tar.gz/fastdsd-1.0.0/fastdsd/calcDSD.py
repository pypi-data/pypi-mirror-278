#!/usr/sup/bin/python
'''
calcDSD.py -- This module parse calculates DSD given the adjacency matrix
    and output accoding to options

DSD version 0.5, Copyright (C) 2013, Tufts University
@author -- Mengfei Cao, mcao01@cs.tufts.edu
161 College Ave., Medford, MA 02155, USA

This program is free software; you can redistribute it and/or modify
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

'''

import numpy as np
import re

import numpy as np
from numpy.linalg import inv
from scipy.spatial.distance import pdist, squareform

def calculator(adjacency, nRw):
    """
    adjacency - adjacency matrix represented as a numpy array
                assumes graph is fully connected.
    nRW - the length of random walks used to calculate DSD
          if nRW = -1, then calculate DSD at convergence
    returns DSD matrix represented as a numpy array
    """
    n = adjacency.shape[0]
    degree = adjacency.sum(axis=1)
    p = adjacency / degree
    if nRw >= 0:
        c = np.eye(n)
        for i in range(nRw):
            c = np.dot(c, p) + np.eye(n)
        return squareform(pdist(c,metric='cityblock'))
    else:
        pi = degree / degree.sum()
        return squareform(pdist(inv(np.eye(n) - p - pi.T),metric='cityblock'))


def writeoutMatrix(DSD, names, ofile):
    """
    write DSD matrix into a tab delimited csv file

    DSD -- the DSD matrix, an numpy matrix

    names -- the node IDs, a dict

    ofile -- the output file object

    """
    n = np.size(DSD[0])
    count = 0
    temp = "\t"
    while(count < n-1):
        temp = temp + names[count] + '\t'
        count = count + 1
    temp = temp + names[n-1] + '\n'
    ofile.write(temp)
    for i in range(0, n):
        temp = names[i]
        for j in range(0, n):
            if DSD[i, j] < 0:
                temp = temp + '\tNA'
            else:
                temp = temp + '\t%.4f' % DSD[i, j]
        ofile.write(temp + '\n')
    return True


def writeoutList(DSD, names, infile, ofile):
    """
    write DSD into a file, where each line is an interaction from
    input file, followed by the DSD values

    DSD -- the DSD matrix, an numpy matrix

    names -- the node IDs, a dict

    infile -- the name of input file

    ofile -- the output file object

    """
    splitpattern = re.compile('[\t ;,]+')
    validpattern = re.compile('^[\w _\-.,\t\':;"]+$')
    ifile = open(infile, 'r')
    for temp in ifile:
        temp = temp.strip('\t \n\r')
        if temp == "" or re.search(validpattern, temp) is None:
            continue
        else:
            allwords = re.split(splitpattern, temp)
            if(allwords[0] not in names) or (allwords[1] not in names):
                temp = allwords[0] + '\t' + allwords[1] + '\tNotConnected\n'
            else:
                i = names.index(allwords[0])
                j = names.index(allwords[1])
                temp = names[i] + '\t' + names[j] + '\t%.4f\n' % DSD[i, j]
            ofile.write(temp)
    ifile.close()
    return True
 #   print adjacency
 #   print p
 #   print degree


def writeoutToplist(DSD, names, ofile, nTop):
    """
    write DSD into a file, where for each node, we put at the first
    column, then followed by nTop nodes with lowest DSD, in increasing
    order

    DSD -- the DSD matrix, an numpy matrix

    names -- the node IDs, a dict

    ofile -- the output file object

    nTop -- the number of nodes with lowest DSD

    """
    n = np.size(DSD[0])
    for i in range(0, n):
        temp = names[i]
        TopKIndex = findTopk(DSD[i], nTop, i)
        for j in range(0, nTop):
            if TopKIndex[j] >= 0:
                temp = temp + '\t' + names[TopKIndex[j]]
                temp = temp + ('(%.4f)' % DSD[i, TopKIndex[j]])
            else:
                break
        ofile.write(temp + '\n')
    return True


def findTopk(values, k, a):
    '''
    it finds the k smallest items in list "values" excluding the "a"th item

    values -- a list of numerical values

    k -- the number of smallest items

    a -- the item to be excluded

    returns a list of indices with smallest values, increasing order

    '''
    n = np.size(values)
    indicator = [True]*n
    indicator[a] = False
    index = [-1]*k
    m = max(values)
    for i in range(0, n):
        if values[i] < 0:
            indicator[i] = False
    for i in range(0, k):
        temp = m
        for j in range(0, n):
            if(values[j] <= temp) and indicator[j]:
                temp = values[j]
                index[i] = j
        if index[i] >= 0:
            indicator[int(index[i])] = False
        else:
            break
    return index
