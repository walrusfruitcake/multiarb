#!/usr/bin/env python

import sys
import multiarbtree as tree
import multiarbnodes as nodes
import networkx as nx

print('max int size--relevant to use of nBTC vs BTC:')
maxInt = sys.maxsize
print(maxInt)
print(float(maxInt))

respStr = str(input("proceed? [y]")).lower()
if not((respStr == 'y') | (respStr == 'yes') | (respStr == '')):
  sys.exit()

# create some currency nodes
btc = nodes.CurrencyNode('BTC', 1, 0.02)
usd = nodes.CurrencyNode('USD', 1/600.0, 0.02)
ltc = nodes.CurrencyNode('LTC', 0.027, 0.02)

# add them to a new graph
G = nx.MultiDiGraph();
G.add_edge(btc, usd, commission=0.02, exchange=605.0)
G.add_edge(btc, ltc, commission=0.02, exchange=1/0.028)
G.add_edge(ltc, usd, commission=0.02, exchange=17.28)

#sys.exit()

# build tree
testTree = tree.Tree(G, btc, 1.0, 4)
testTree.populateTree()
