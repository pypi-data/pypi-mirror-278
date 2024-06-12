#!/usr/bin/python

import numpy as np
import operator
import sys

def print_imap(target, i_map):
    print("not implemented at the moment")

def print_adjacency(target, adj):
    temp = np.array(adj != 0, dtype = int)
    np.savetxt(target,adj,delimiter="",fmt="%.1d")

def read_adjacency(target):
    f = open(target,'r')
    a = []
    for l in f.readlines():
        a.append(map(int,list(l.rstrip())))

    a = np.array(a)
        
    #for i in range(np.size(a[0])):
        #if not np.sum(a[i,:])+np.sum(a[:,i]): print str(i), np.sum(a[i,:])+np.sum(a[:,i])
        
    return a

def print_transition(target, transition):
    np.savetxt(target,transition,delimiter="\t")

def print_i_map(target, i_map):
    f = open(target, 'w')
    for (a,b),c in i_map.items():
        a,b,c = str(a), str(b), str(c)
        f.write("\t".join([a,b,c,'\n']))
    f.close()

def read_dsd(target):
    f = open(target, 'r')
    l = f.readline()
    l = l.rstrip().split('\t')[1:]
    n = len(l)
    
    names = {}
    for i in range(n):
        names[l[i]] = i
        
    scores = np.empty(n, dtype=object)
    for i in range(n):
        l = f.readline().rstrip().split('\t')[1:]
        scores[i] = np.array(l).astype('float')
    return (names, scores)
        

def print_dsd(target, scores, names):
    sorted_names = sorted(names.iteritems(), key = operator.itemgetter(1))

    n = len(sorted_names)

    f = open(target,'w')

    s = "\t"
    for i in range(n):
        s+=sorted_names[i][0]+"\t"
    f.write(s[:-1]+"\n")
    for i in range(n):
        s = sorted_names[i][0]
        for j in range(n):
            s+="\t"+str(scores[i][j])
        f.write(s+"\n")
    f.close()

def print_trimat(target, scores):
    f = open(target,'w')
    n = np.size(scores[0])
    for i in range(n):
        l = ""
        for j in range(i+1,n):
            l += "{:0.8f}".format(scores[i][j])+"\t"
        f.write(l+"\n")
    f.close()

def print_names(target, names):
    sorted_names = sorted(names.iteritems(), key = operator.itemgetter(1))

    n = len(sorted_names)

    f = open(target,'w')

    for i in range(n):
        f.write(sorted_names[i][0]+"\n")
    f.close()

def read_names(target):
    names = {}
    counter = 0
    f = open(target, 'r')
    for n in f.readlines():
        if n.rstrip not in names:
            names[n.rstrip()] = counter
            counter += 1
        else:
            pass
    return names

def writeoutMatrix(DSD, names, ofile):
    """
    write DSD matrix into a tab delimited csv file

    DSD -- the DSD matrix, an numpy matrix

    names -- the node IDs, a dict

    ofile -- the output file object

    """
    n = DSD.shape[0]
    count = 0
    temp = "\t"
    ofile.write('{}\n'.format('\t'.join(names)))
    for i in range(0, n):
      ofile.write('{}\t{}\n'.format(names[i],'\t'.join([str(i) for i in DSD[i,:]])))
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

if __name__ == "__main__":
    print(read_adjacency(sys.argv[1]))
