#!/usr/bin/python

import numpy as np
import re
import operator
import networkx as nx
from numpy.linalg import inv
from scipy.spatial.distance import pdist, squareform

def build_transition_matrix(graph):
    adjacency_matrix = nx.to_numpy_array(graph)
    degs = adjacency_matrix.sum(axis=1)

    transition = adjacency_matrix / degs
    return transition, degs

def calc_hescotts(transition, nRw):
    p = transition
    n = p.shape[0]
    c = np.eye(n)
    c0 = np.eye(n)
    for i in range(nRw):
        c = np.dot(c, p) + c0
    return c

def calc_dsd(graph, nRw, quiet=True):
    if not quiet:
          print("Calculating Hescotts...")
    if nRw >= 0:
        transition, _ = build_transition_matrix(graph)
        hescotts = calc_hescotts(transition, nRw)
    else:
        transition, degree = build_transition_matrix(graph)
        pi = degree / degree.sum()
        p = transition
        n = p.shape[0]
        hescotts = inv(np.eye(n) - p - pi.T)
    if not quiet:
        print("Calculating DSD...")
    return squareform(pdist(hescotts,metric='cityblock'))

def add_self_edges(adjacency_graph, base_weight=1):
    n = np.size(adjacency_graph[0])
    ident = np.identity(n)*base_weight
    return np.add(adjacency_graph,ident)
