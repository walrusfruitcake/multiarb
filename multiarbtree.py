#!/usr/bin/env python

import multiarbnodes as nodes
# for arbitrary-precision arithmetic without float-type errors
import decimal as d
# IPython for debugging
from IPython import embed as shell
# for debugging, wrapping each TreeNode in a networkx node
import networkx as nx
import matplotlib.pyplot as plt
  
# Tree class for multiarb. Builds itself from a NetworkX MultiDiGraph
class Tree:

  # Default constructor
  # @param graph the MultiDiGraph of CurrencyNode objects
  # @param base the base currency as a CurrencyNode object
  # @param initAmt the initial trade amount in base currency, a Decimal object
  # @param maxHops max steps taken in the path, or the max height of the tree
  def __init__(self, graph, base, initAmt, maxHops):
    # set precision
    d.getcontext().prec=20
    self.graph = graph
    # root node: create from CurrencyNode base, initialize value, set as current
    self.rootNode = nodes.TreeNode(base, initAmt, 0)
    self.rootNode.baseVal = initAmt
    self.currNode = self.rootNode

    self.maxHeight = maxHops
    self.breadthComplete = True;
    #print('init\'ized')
    # networkx graph as a debugging tree
    self.T = nx.DiGraph()

  # Recursive method for BFS-filling the tree
  def populateTree(self):
    # iterator over the outgoing edges from currNode. Include edge data not keys
    outEdgeIter = self.graph.out_edges_iter([self.currNode.currency], True, False)
    #print(self.currNode is self.rootNode)
    # recover the rate information from the graph data
    for edge in outEdgeIter:
      print(edge)
      #targetObj = edge[1] #of type CurrencyNode
      #rate = edge[2]['rate']
      if not (edge[1] is self.rootNode.currency):
        #newChild = nodes.TreeNode(edge[1], __calcAmt(self.currNode, edge[2]))
        #self.currNode.addChild(newChild)
        self.currNode.addChild(edge[1], self.__calcAmt(self.currNode, edge[2]))
        # only necessary for debug-tree. edge from currNode to just-added child
        self.T.add_edge(self.currNode, self.currNode.children[-1])

    print(self.currNode.children)

    if not self.breadthComplete:
      return None #return void

    self.breadthComplete = False

    # only necessary for debug-tree visualization
    nx.draw(self.T,None,None,False)
    plt.savefig('tree.png')
    input()

    for childNode in self.currNode.children:
      # becomes one of the children
      self.currNode = childNode
      self.populateTree();
      # only necessary for debug-tree visualization
      plt.clf()
      nx.draw(self.T,None,None,False)
      plt.savefig('tree.png')
      input()

    shell()
    self.breadthComplete = True;


  # internal method. compute amount of target currency after edge transaction
  # @param parentNode the 'from' currency in the transaction
  def __calcAmt(self, parentNode, edgeDict):
    return edgeDict['exchange'] * parentNode.amount * (d.Decimal(1)-edgeDict['commission'])
