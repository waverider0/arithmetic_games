#!/usr/bin/env python3

import ast
import random
import readline

# computer generates a random equation (or system) like (ab^3)/(c+d) = 24
# you find values for a,b,c,d that satisfy the equation

OPS = ['Add', 'Sub', 'Mult', 'Div']
EQUATIONS = 1
VARIABLES = 2

if __name__ == '__main__':
  print('search.py')
