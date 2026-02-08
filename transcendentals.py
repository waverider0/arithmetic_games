#!/usr/bin/env python3

import math
import random
import readline
import threading

def rel_error(ans, exact):
  return abs(ans - exact) / (abs(exact) or 1)

def make_sqrt():
  x = random.randint(0, 1000)
  return f'sqrt({x}) = ', math.sqrt(x)

def make_exp():
  x = random.uniform(-5, 5)
  return f'e^{x:.2f} = ', math.exp(x)

def make_ln():
  x = random.randint(2, 1000)
  return f'ln({x}) = ', math.log(x)

def make_log():
  b = random.randint(2, 10)
  x = random.randint(2, 1000)
  return f'log{b}({x}) = ', math.log(x) / math.log(b)

def make_sin():
  x_deg = random.randint(0, 90)
  return f'sin({x_deg}°) = ', math.sin(math.radians(x_deg))

def make_cos():
  x_deg = random.randint(0, 90)
  return f'cos({x_deg}°) = ', math.cos(math.radians(x_deg))

def make_tan():
  x_deg = random.randint(0, 80)
  return f'tan({x_deg}°) = ', math.tan(math.radians(x_deg))

def make_asin():
  x = round(random.uniform(0, 1), 2)
  return f'asin({x}) = ', math.degrees(math.asin(x))

def make_acos():
  x = round(random.uniform(0, 1), 2)
  return f'acos({x}) = ', math.degrees(math.acos(x))

def make_atan():
  x = round(random.uniform(0, 5), 2)
  return f'atan({x}) = ', math.degrees(math.atan(x))

FUNCTIONS = {
  'sqrt': make_sqrt,
  'exp' : make_exp,
  'ln'  : make_ln,
  'log' : make_log,
  'sin' : make_sin,
  'cos' : make_cos,
  'tan' : make_tan,
  #'asin': make_asin,
  #'acos': make_acos,
  #'atan': make_atan,
}
DURATION_SECONDS = 120

if __name__ == '__main__':
  score = 0
  running = threading.Event()
  running.set()
  threading.Timer(DURATION_SECONDS, running.clear).start()

  while running.is_set():
    name = random.choice(list(FUNCTIONS.keys()))
    prompt, exact = FUNCTIONS[name]()

    ans = None
    while ans is None or rel_error(ans, exact) > 0.1:
      try: ans = float(input(prompt))
      except ValueError: continue

    score += 1
    print(f'Exact: {round(exact, 2)} ({round(rel_error(ans, exact) * 100, 2)}% error)')
    print(f'Score: {score}')
