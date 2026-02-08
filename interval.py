#!/usr/bin/env python3

import ast
import math
import random
import readline

"""
zetamac.py (L1) -> target.py (L2)
transcendentals.py (L1) -> interval.py (L2)

you're given a set of functions (e.g: sqrt, e^x, log10), then given some value of x (e.g: 5) and then given a desired target range (e.g: [0,5.5]) and the goal is to compose the functions such that the final answer falls within the range. we can answer with "log10 sqrt exp x" or whatever syntax works best. keep as pure function composition (don't include binops like +)

some key considerations:
* guarenteed solvability
* domain safety
* exploding ranges
* as close as possible to uniform sampling for each position in the chain
"""

FUNCTIONS = {
  'sqrt' : (math.sqrt                           , lambda x: x >= 0),
  'exp'  : (math.exp                            , lambda x: -5 <= x <= 5),
  'ln'   : (math.log                            , lambda x: x >= 0.1),
  'log2' : (math.log2                           , lambda x: x >= 0.1),
  'log10': (math.log10                          , lambda x: x >= 0.1),
  'sin'  : (lambda x: math.sin(math.radians(x)) , lambda x: True),
  'cos'  : (lambda x: math.cos(math.radians(x)) , lambda x: True),
  'tan'  : (lambda x: math.tan(math.radians(x)) , lambda x: abs(x % 180 - 90) >= 10),
  'asin' : (lambda x: math.degrees(math.asin(x)), lambda x: -1 <= x <= 1),
  'acos' : (lambda x: math.degrees(math.acos(x)), lambda x: -1 <= x <= 1),
  'atan' : (lambda x: math.degrees(math.atan(x)), lambda x: True),
}
INTERMEDIATE_RANGE = [-1000, 1000]
INPUT_OUTPUT_RANGE = [-100,100]
TOLERANCE = 0.1
CHAIN_LENGTH = 3

if __name__ == '__main__':
  for i in range(1000):
    chain = []
    for i in range(CHAIN_LENGTH): chain.append(random.choice(list(FUNCTIONS.keys())))
    xs = list(range(*INPUT_OUTPUT_RANGE))
    random.shuffle(xs)
