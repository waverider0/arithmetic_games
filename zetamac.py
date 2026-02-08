#!/usr/bin/env python3

import random
import readline
import threading

OPS = ['+', '-', '*', '/', '^', '%']
ADD_L = [2,200]
ADD_R = [2,200]
MUL_L = [2,20]
MUL_R = [2,100]
POW_L = [2,10]
POW_R = [2,10]
DURATION_SECONDS = 120

if __name__ == '__main__':
  score = 0
  running = threading.Event()
  running.set()
  threading.Timer(DURATION_SECONDS, running.clear).start()

  while running.is_set():
    op = random.choice(OPS)

    if op in '+-':
      a = random.randint(*ADD_L)
      b = random.randint(*ADD_R)
      exact = a + b if op == '+' else a - b
      parse = int
      check = lambda x: x == exact
    elif op == '*':
      a = random.randint(*MUL_L)
      b = random.randint(*MUL_R)
      exact = a * b
      parse = int
      check = lambda x: x == exact
    elif op == '/':
      a = random.randint(MUL_L[0]*MUL_R[0], MUL_L[1]*MUL_R[1])
      b = random.randint(*MUL_R)
      exact = a / b
      parse = float
      check = lambda x: abs((x - exact) / exact) <= 0.01
    elif op == '^':
      a = random.randint(*POW_L)
      b = random.randint(*POW_R)
      exact = a ** b
      parse = int
      check = lambda x: x == exact
    else:
      a = random.randint(MUL_L[0]*MUL_R[0], MUL_L[1]*MUL_R[1])
      b = random.randint(*MUL_R)
      exact = a % b
      parse = int
      check = lambda x: x == exact

    ans = None
    while ans is None or not check(ans):
      try: ans = parse(input(f'{a} {op} {b} = '))
      except ValueError: continue

    if op == '/': print(f'Exact: {round(exact, 2)} ({round((ans - exact) / exact * 100, 2)}% error)')
    score += 1
    print(f'Score: {score}')
