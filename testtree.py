#!/usr/bin/env python

import sys
import multiarbtree as tree
import multiarbnodes as nodes
# for arbitrary-precision arithmetic without float-type errors
import decimal as d
# for debugging, draw tree as a graph
import networkx as nx
import matplotlib.pyplot as plt

print('max int size--relevant to use of nBTC vs BTC:')
maxInt = sys.maxsize
print(maxInt)
print(float(maxInt))

# Deprecated as of switch to Decimal type
#respStr = str(input('proceed? [y]')).lower()
#if not((respStr == 'y') | (respStr == 'yes') | (respStr == '')):
#  sys.exit()

# this approach deprecated with edges-back-to-BTC
# create some currency nodes
comm = d.Decimal('0.02')
btc = nodes.CurrencyNode('BTC', d.Decimal(1), comm)
usd = nodes.CurrencyNode('USD', d.Decimal(1)/d.Decimal(600), comm)
ltc = nodes.CurrencyNode('LTC', d.Decimal('0.027'), comm)

# add currency pairs as edges in a them to a new graph
G = nx.MultiDiGraph();

G.add_edge(btc,usd, commission=comm, exchange=d.Decimal(605))
G.add_edge(btc,ltc, commission=comm, exchange=d.Decimal(1)/d.Decimal('0.02789'))
G.add_edge(ltc,usd, commission=comm, exchange=d.Decimal('17.28'))

# test-edges back to BTC
G.add_edge(usd,btc, commission=comm, exchange=d.Decimal(1)/d.Decimal(600))
#G.add_edge(ltc,btc, commission=comm, exchange=d.Decimal('0.027'))


#sys.exit()

# build tree
testTree = tree.Tree(G, btc, d.Decimal(1), 4)
testTree.populateTree()
input('last chance to examine tree.png')
plt.clf()
nx.draw(testTree.T,None,None,False)
plt.savefig('tree.png')
