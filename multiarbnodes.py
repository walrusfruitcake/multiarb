#!/usr/bin/env python

# for arbitrary-precision arithmetic without float-type errors
import decimal as d

# Node representing a currency, to be updated with its value in base (USD|BTC)
class CurrencyNode:
  # Default constructor.
  # @param acronym the code for the currency 
  # both Decimal objects:
  # @param exchange the exch rate of selling 1 unit of this currency
  # @param commission the commission rate of that transaction
  def __init__(self, acronym, exchange, commission):
    self.acronym = acronym;
    self.baseRate = exchange * (d.Decimal(1) - commission)

  # String representation for printing
  def __str__(self):
    return self.acronym

  # String representation for evaluation
  def __repr__(self):
    return self.acronym

  # unit val in base currency, i.e. exch rate of selling 1 unit of this currency
  # deprecated
  def setRate(self, rate):
    self.baseRate = rate
  # sets indexVal directly
  #def setVal()
    #self.baseVal = 

# Node to be used in the tree representing possible paths
class TreeNode:
  # Default constructor
  # @param currency the CurrencyNode object of this TreeNode
  # @param amount in this currency, a Decimal object
  # @depth length of the path from root TreeNode, in hops
  def __init__(self, currency, amount, depth):
    self.currency = currency
    # set amount in node currency and value in base currency, of this node
    self.amount = amount
    # moved to addChild()
    #self.baseVal = self.currency.baseRate * self.amount
    #self.baseVal
    # initialize empty list
    self.children = []
    self.depth = depth

  # String representation for printing
  def __str__(self):
    roundVal = self.baseVal.quantize(d.Decimal('0.0001'),rounding=d.ROUND_DOWN)
    return str(self.currency) + '::' + str(roundVal)

  # String representation for evaluation
  def __repr__(self):
    # sufficient for node identification since no duplicate currencies
    return self.currency.acronym

  # sets depth
  # deprecated
  def setDepth(self, depth):
    self.depth = depth

  # Accepts a CurrencyNode cNode of Decimal amount in that (not base) currency,
  # creating a TreeNode as a child node in the path
  def addChild(self, cNode, amount):
    #tNode.setDepth(self.depth + 1)
    # prepend self.?
    tNode = TreeNode(cNode, amount, self.depth+1)
    tNode.baseVal = tNode.currency.baseRate * tNode.amount
    self.children.append(tNode)

