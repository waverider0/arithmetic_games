#!/usr/bin/env python3

import random, readline, threading

DURATION = 120

def make_pow():
  while True:
    a, b = random.randint(2, 20), random.randint(2, 10)
    if a ** b <= 1e9: return a, b

OPS = {
  '+':  lambda: (random.randint(2,1000), random.randint(2,1000)),
  '-':  lambda: (random.randint(2,1000), random.randint(2,1000)),
  '*':  lambda: (random.randint(2,100), random.randint(2,20)),
  '/':  lambda: (random.randint(2,2000), random.randint(2,20)),
  '**': make_pow,
}

if __name__ == '__main__':
  score = 0
  running = threading.Event()
  running.set()
  timer = threading.Timer(DURATION, running.clear)
  timer.start()
  try:
    while running.is_set():
      op = random.choice(list(OPS))
      a, b = OPS[op]()
      exact = eval(f'{a} {op} {b}')
      parse = float if isinstance(exact, float) else int
      while True:
        try: ans = parse(input(f'{a} {op} {b} = '))
        except ValueError: continue
        if ans == exact:
          if isinstance(exact, float): print(f'Exact: {round(exact, 2)} ({round((ans - exact) / exact * 100, 2)}% error)')
          break
      score += 1
      print(f'Score: {score}')
  except (KeyboardInterrupt, EOFError): timer.cancel()
  print(f'\nAnswer: {exact}')