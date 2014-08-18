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
        amt = self.__calcAmt(self.currNode.amount, edge[2])
        val = self.__calcVal(edge[1], amt)
        self.currNode.addChild(edge[1], amt, val)
        # only necessary for debug-tree. edge from currNode to just-added child
        self.T.add_edge(self.currNode, self.currNode.children[-1])
        #shell()

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

    #shell()
    self.breadthComplete = True;


  # internal method. compute amount of target currency after edge transaction
  # @param amount amount of parentNode, deprecates parentNode arg
  # @param parentNode TreeNode representing the transaction's 'from' currency
  def __calcAmt(self, amount, edgeDict):
    rate = edgeDict['exchange'] * (d.Decimal(1)-edgeDict['commission'])
    return amount * rate

  # method to compute value of child in base currency
  def __calcVal(self, childCurrency, amount):
    try:
      edgeDict = self.graph[childCurrency][self.rootNode.currency][0]
      # reuse calcAmt since the format of everything is the same
      return self.__calcAmt(amount, edgeDict)
    # if no edge exists from child currency to base currency
    except KeyError:
      # TODO print Traceback associated with this KeyError instance?
      exceptStr = 'No direct value of ' + str(childCurrency)
      exceptStr += ' in base '+str(self.rootNode.currency)
      print(exceptStr)
      quit()
    
