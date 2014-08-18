#!/usr/bin/env python

import multiarbnodes as nodes
# IPython for debugging
from IPython import embed as shell
  
# Tree class for multiarb. Builds itself from a NetworkX MultiDiGraph
class Tree:

  # Default constructor
  # @param graph the MultiDiGraph of CurrencyNode objects
  # @param base the base currency as a CurrencyNode object
  # @param initAmt the initial trade amount in base currency
  # @param maxHops max steps taken in the path, or the max height of the tree
  def __init__(self, graph, base, initAmt, maxHeight):
    self.graph = graph
    self.rootNode = nodes.TreeNode(base, initAmt, 0)
    self.currNode = self.rootNode
    self.maxHeight = maxHeight
    self.breadthComplete = True;
    #print('init\'ized')

  # Recursive method for BFS-filling the tree
  def populateTree(self):
    # iterator over the outgoing edges from currNode. Include edge data not keys
    outEdgeIter = self.graph.out_edges_iter([self.currNode.currency], True, False)
    print(self.currNode is self.rootNode)
    # recover the rate information from the graph data
    for edge in outEdgeIter:
      print(edge)
      #targetObj = edge[1] #of type CurrencyNode
      #rate = edge[2]['rate']
      #if !(self.currNode is self.rootNode)
      #newChild = nodes.TreeNode(edge[1], __calcAmt(self.currNode, edge[2]))
      #self.currNode.addChild(newChild)
      self.currNode.addChild(edge[1], self.__calcAmt(self.currNode, edge[2]))

    if not self.breadthComplete:
      return None #return void

    self.breadthComplete = False

    print(self.currNode.children)
    for childNode in self.currNode.children:
      # becomes one of the children
      print('hi')
      self.currNode = childNode
      self.populateTree();

    shell()
    self.breadthComplete = True;


  # internal method. compute amount of target currency after edge transaction
  # @param parentNode the 'from' currency in the transaction
  def __calcAmt(self, parentNode, edgeDict):
    return edgeDict['exchange'] * parentNode.amount * (1-edgeDict['commission'])
