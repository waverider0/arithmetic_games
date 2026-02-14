#!/usr/bin/env python3

import math, os, random, sys, time
from collections import Counter

OPS = ['+', '-', '*', '/', '**']
TARGET_RANGE = [10, 400]
NUMBER_RANGE = [2, 100]
NUMBER_COUNT = 5
VIZ_SAMPLE_SIZE = 20000

class Node:
  def __init__(self, val=None, op=None, left=None, right=None, is_leaf=False):
    self.val = val
    self.op = op
    self.left = left
    self.right = right
    self.is_leaf = is_leaf
  def __repr__(self): return str(self.val) if self.is_leaf else f"({self.left} {self.op} {self.right})"

def generate_skeleton(n):
  """Generates a random binary tree structure."""
  if n == 1: return Node(is_leaf=True)
  split = random.randint(1, n-1) if n > 2 else 1
  return Node(op=random.choice(OPS), left=generate_skeleton(split), right=generate_skeleton(n-split))

def evaluate_and_repair(node):
  """Bottom-up traversal that forces values to satisfy operator constraints."""
  if node.is_leaf:
    node.val = random.randint(*NUMBER_RANGE)
    return node.val

  l_val = evaluate_and_repair(node.left)
  r_val = evaluate_and_repair(node.right)
  op = node.op

  # --- Constraint Logic (Polynomial Time) ---
  if op == '/':
    if r_val == 0:
      r_val = 1
      node.right.val = 1
    if l_val % r_val != 0:
      multiplier = random.randint(1, 15)  # Keep small to avoid explosion
      l_val = r_val * multiplier
      node.left.val = l_val
  elif op == '**':
    if abs(l_val) > 20 and abs(r_val) > 1:
      r_val = 1
      node.right.val = 1
    elif abs(l_val) > 5 and abs(r_val) > 2:
      r_val = random.randint(0, 2)
      node.right.val = r_val
    if abs(r_val) > 5:
      l_val = random.randint(0, 2)
      node.left.val = l_val
    try:
      res = l_val ** r_val
      if isinstance(res, complex) or abs(res) > 200000:
        op = '+'
        node.op = '+'
    except:
      op = '+'
      node.op = '+'

  # --- Calculation ---
  try:
    if op == '+':    res = l_val + r_val
    elif op == '-':  res = l_val - r_val
    elif op == '*':  res = l_val * r_val
    elif op == '/':  res = l_val / r_val
    elif op == '**': res = l_val ** r_val
  except:
    res = 0  # Fallback for div by zero or overflow

  node.val = res
  return res

def get_leaves(node):
  if node.is_leaf: return [node.val]
  return get_leaves(node.left) + get_leaves(node.right)

def generate_puzzle():
  """Generates a single valid puzzle instance."""
  for _ in range(100):
    root = generate_skeleton(NUMBER_COUNT)
    res = evaluate_and_repair(root)
    if TARGET_RANGE[0] <= res <= TARGET_RANGE[1]: return root, res
  return None

# --- Visualization Mode (VIZ=1) ---
if os.getenv("VIZ"):
  import matplotlib.pyplot as plt
  print(f"--- ANALYZING (Samples: {VIZ_SAMPLE_SIZE}, Range: {NUMBER_RANGE}) ---")

  ops_cnt = Counter()
  leaf_vals = []
  targets = []

  def walk_stats(n):
    if n.is_leaf: leaf_vals.append(n.val)
    else:
      ops_cnt[n.op] += 1
      walk_stats(n.left)
      walk_stats(n.right)

  st = time.time()
  generated = 0
  while generated < VIZ_SAMPLE_SIZE:
    p = generate_puzzle()
    if p:
      targets.append(p[1])
      walk_stats(p[0])
      generated += 1

  print(f"Generated {VIZ_SAMPLE_SIZE} samples in {time.time()-st:.2f}s")

  fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

  ax1.bar(ops_cnt.keys(), ops_cnt.values(), color='#66B2FF')
  ax1.set_title("Operator Frequency")

  ax2.hist(leaf_vals, bins=range(0, 105), color='#55AA55', alpha=0.7)
  ax2.set_title(f"Leaf Value Distribution (Min: {NUMBER_RANGE[0]})")
  ax2.set_xlabel("Value")

  ax3.hist(targets, bins=50, color='#FFAA33', alpha=0.7)
  ax3.set_title(f"Target Value Distribution ({TARGET_RANGE})")

  plt.tight_layout()
  plt.show()
  sys.exit(0)

# --- Game Mode ---
if __name__ == "__main__":
  import re
  print(f"Generative Arithmetic Game (Range: {NUMBER_RANGE})")
  print("Press 'q' to reveal solution, 'n' for next, or Ctrl+C to exit.")

  while True:
    p = generate_puzzle()
    if not p: continue

    root, target = p
    leaves = sorted(get_leaves(root))

    print(f"\nTarget:  {target}")
    print(f"Numbers: {leaves}")

    while True:
      user_in = input("Formula > ").strip()

      if user_in.lower() == 'q': print(f"Solution: {root}"); break
      if user_in.lower() == 'n': break
      if not user_in: continue

      try:
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', user_in) and "**" not in user_in:
          print("Invalid characters.")
          continue

        user_nums = sorted([int(x) for x in re.findall(r'\d+', user_in)])
        if user_nums != leaves:
          print(f"Wrong numbers! Used: {user_nums}")
          continue

        res = eval(user_in)
        if res == target: print(f"Correct! ({res})"); break
        else: print(f"Incorrect. Result: {res}")
      except Exception as e:
        print(f"Error: {e}")