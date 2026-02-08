#!/usr/bin/env python3

import ast
import math
import random
import readline

X_RANGE = [2,20]
Y_RANGE = [0,100]
LIST_SIZE = 2

"""
zetamac.py (L1) -> target.py (L2)
transcendentals.py (L1) -> interval.py (L2)

you're given a set of functions (e.g: sqrt, e^x, log10), then given some value of x (e.g: 5) and then given a desired target range (e.g: [0,5.5]) and the goal is to compose the functions such that the final answer falls within the range. we can answer with "log10 sqrt exp x" or whatever syntax works best. keep as pure function composition (don't include binops like +)

some key considerations:
* guarenteed solvability
* domain safety
* exploding ranges
"""
