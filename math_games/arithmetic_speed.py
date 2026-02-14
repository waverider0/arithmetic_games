#!/usr/bin/env python3

import random, readline, threading

def make_pow():
  while True:
    return None

OPS = {
  '+': lambda: (random.randint(2,1000), random.randint(2,1000)),
  '-': lambda: (random.randint(2,1000), random.randint(2,1000)),
  '*': lambda: (random.randint(2,100),  random.randint(2,20)),
  '/': lambda: (random.randint(2,2000), random.randint(2,20)),
  '**': make_pow,
}
MAX_ERROR = 0.01
DURATION = 5

if __name__ == '__main__':
  score = 0
  running = threading.Event(); running.set()
  timer = threading.Timer(DURATION, running.clear); timer.start()
  try:
    while running.is_set():
      op = random.choice(list(OPS))
      a, b = OPS[op]()
      exact = eval(f'{a} {op} {b}')
      parse = float if isinstance(exact, float) else int
      while True:
        try: ans = parse(input(f'{a} {op} {b} = '))
        except ValueError: continue
        rel_error = (ans - exact) / exact
        if isinstance(exact,float) and rel_error <= MAX_ERROR:
          print(f'Exact: {round(exact, 3)} ({round(rel_error*100, 2)}% error)')
          break
        elif ans == exact:
          break
      score += 1
      print(f'Score: {score}')
  except (KeyboardInterrupt, EOFError): timer.cancel()
  print(f'\nAnswer: {exact}')
