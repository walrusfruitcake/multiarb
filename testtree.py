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

respStr = str(input('proceed? [y]')).lower()
if not((respStr == 'y') | (respStr == 'yes') | (respStr == '')):
  sys.exit()

# create some currency nodes
comm = d.Decimal('0.02')
exch = d.Decimal(1)
btc = nodes.CurrencyNode('BTC', exch, comm)
exch = d.Decimal(1)/d.Decimal(600)
usd = nodes.CurrencyNode('USD', exch, comm)
exch = d.Decimal('0.027')
ltc = nodes.CurrencyNode('LTC', exch, comm)

# add them to a new graph
G = nx.MultiDiGraph();
comm = d.Decimal('0.02')
exch = d.Decimal(605)
G.add_edge(btc, usd, commission=comm, exchange=exch)
exch = d.Decimal(1)/d.Decimal('0.02789')
G.add_edge(btc, ltc, commission=comm, exchange=exch)
exch = d.Decimal('17.28')
G.add_edge(ltc, usd, commission=comm, exchange=exch)

#sys.exit()

# build tree
testTree = tree.Tree(G, btc, d.Decimal(1), 4)
testTree.populateTree()
input('last chance to examine tree.png')
plt.clf()
nx.draw(testTree.T,None,None,False)
plt.savefig('tree.png')
