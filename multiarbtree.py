#!/usr/bin/env python

# Tree class for multiarb. Builds itself from a NetworkX MultiDiGraph
class Tree:
  import multiarbnodes as nodes

  # Default constructor
  # @param graph the MultiDiGraph of CurrencyNode objects
  # @param base the base currency as a CurrencyNode object
  # @param initAmt the initial trade amount in base currency
  # @param maxHeight the max height of the tree, or max steps taken in path
  def __init__(self, graph, base, initAmt, maxHeight):
    self.graph = graph
    self.rootNode = nodes.TreeNode(base, initAmt, 0)
    self.currNode = rootNode
    self.breadthComplete = True;

  # Recursive method for BFS-filling the tree
  def populateTree(self):
    # iterator over the outgoing edges from currNode. Include edge data not keys
    outEdgeIter = graph.out_edges_iter(currNode, True, False)
    # recover the rate information from the graph data
    for edge in outEdgeIter:
      #targetObj = edge[1] #of type CurrencyNode
      #rate = edge[2]['rate']
      #if !(currNode is self.rootNode)
      #newChild = nodes.TreeNode(edge[1], __calcAmt(currNode, edge[2]))
      #self.currNode.addChild(newChild)
      self.currNode.addChild(edge[1], __calcAmt(currNode, edge[2]))

    if not self.breadthComplete:
      return None #return void

    self.breadthComplete = False

    for childNode in currNode.children:
      # becomes one of the children
      self.currNode = None; #TODO
      populateTree();

    self.breadthComplete = True;


  # internal method. compute amount of target currency after edge transaction
  # @param parentNode the 'from' currency in the transaction
  def __calcAmt(self, parentNode, edgeDict):
    return edgeDict['exchange'] * parentNode.amount * (1-edgeDict['commission'])
