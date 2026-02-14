#!/usr/bin/env python3

import math, random
from sympy import parse_expr

OPS = ['+', '-', '*', '/', '**']
TARGET_RANGE = [10, 400]
NUMBER_RANGE = [2, 100]
NUMBER_COUNT = 4
VIZ_SAMPLES = 10000

class Node:
  def __init__(self, is_leaf, val, op, left, right):
    self.is_leaf = is_leaf
    self.val = val
    self.op = op
    self.left = left
    self.right = right
  def __repr__(self): return str(self.val) if self.is_leaf else f"({self.left} {self.op} {self.right})"

def catalan(n:int): return math.comb(2*n, n) // (n+1)

def generate_tree_shape():
  pass

def generate_puzzle():
  pass

if os.getenv("VIZ"):
  import matplotlib.pyplot as plt

  for i in range(VIZ_SAMPLES):
    pass

if __name__ == "__main__":
  while True:
    puzzle = generate_puzzle()
    if not puzzle: continue

    while True:
      user_input = input("Expression: ").strip()