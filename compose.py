#!/usr/bin/env python3

import ast
from collections import defaultdict
import random
import readline

OPS = ['Add', 'Sub', 'Mult', 'Div'] # TODO: add Pow and Mod
TARGET_RANGE = [10,300]
LIST_SIZE = 4

def generate_random_expression(leaves):
  if len(leaves) == 1: return ast.Constant(value=leaves[0])
  split = random.randint(1, len(leaves)-1)
  left = generate_random_expression(leaves[:split])
  right = generate_random_expression(leaves[split:])
  op = getattr(ast, random.choice(OPS))
  return ast.BinOp(left=left, op=op(), right=right)

class TargetVisitor(ast.NodeVisitor):
  def __init__(self):
    self.used_ops = []
  def visit_BinOp(self, node):
    self.used_ops.append(type(node.op).__name__)
    self.generic_visit(node)

class InputVisitor(ast.NodeVisitor):
  def __init__(self, counts):
    self.counts = counts
    self.used = defaultdict(int)
    self.numbers = []
    self.error = ''
  def visit_BinOp(self, node):
    op = type(node.op).__name__
    if op not in OPS: self.error = f'Bad op: {op}'; return
    self.generic_visit(node)
  def visit_Constant(self, node):
    if node.value not in self.counts.keys(): self.error = f"Extra number: '{node.value}'"; return
    if self.used[node.value] + 1 > self.counts[node.value]: self.error = 'Number used more than once'; return
    self.numbers.append(node.value)
    self.used[node.value] += 1
    self.generic_visit(node)

if __name__ == '__main__':
  guaranteed_ops = [op for op in OPS if random.random() < 0.5]
  while True:
    numbers = []
    counts = defaultdict(int)
    for i in range(LIST_SIZE):
      numbers.append(random.randint(1, 20))
      counts[numbers[i]] += 1
    target_tree = generate_random_expression(numbers)
    visitor = TargetVisitor()
    visitor.visit(target_tree)
    if all(op in visitor.used_ops for op in guaranteed_ops):
      target_expression = ast.unparse(target_tree)
      try: target = eval(compile(target_expression, '<ast>', 'eval')) # FIXME: program stalls if target_expression evals to a huge number
      except ZeroDivisionError: continue
      if target.is_integer() and TARGET_RANGE[0] <= target <= TARGET_RANGE[1]: break
  print(numbers)
  print(f'Target: {int(target)}') # explicit cast to int to remove the trailing '.0'

  while True:
    input_expression = input('Expression: ')
    if input_expression == 'I GIVE UP': print(target_expression); break
    visitor = InputVisitor(counts)
    visitor.visit(ast.parse(input_expression))
    if visitor.error: print(visitor.error); continue
    if visitor.used != counts: print(f'Wrong numbers: used {visitor.numbers}'); continue
    try: result = eval(compile(input_expression, '<string>', 'eval'))
    except Exception as e: print(e); continue
    if result == target: print('Correct!'); break
    print(f'Incorrect (got {result}, want {target})')
