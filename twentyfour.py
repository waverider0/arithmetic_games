#!/usr/bin/env python3
import sys, random, readline, signal
from sympy import parse_expr

OPS = ['+', '-', '*', '/', '%', '**']
TARGET_RANGE = [10,200]
NUMBER_RANGE = [2,20]
LIST_SIZE = 4

class Timeout:
  def __enter__(self, *a): signal.signal(signal.SIGALRM, self.h); signal.alarm(1)
  def __exit__(self, *a): signal.alarm(0) 
  def h(self, *a): raise TimeoutError('TLE')

def generate_expression(nums:list[int], required_ops:list[str]) -> str:
  if len(nums) == 1: return str(nums[0])
  split = random.randint(1, len(nums)-1)
  op = required_ops.pop() if required_ops else random.choice(OPS)
  left = generate_expression(nums[:split], required_ops)
  right = generate_expression(nums[split:], required_ops)
  return f'({left} {op} {right})' # NOTE: must wrap the entire expression in () else sympy fails to parse

if __name__ == '__main__':
  while True:
    numbers = [random.randint(*NUMBER_RANGE) for _ in range(LIST_SIZE)]
    required_ops = [op for op in OPS if random.choice([True, False])]
    random.shuffle(required_ops)
    target, solution = None, None
    for _ in range(100): # 100 retries
      random.shuffle(numbers)
      solution = generate_expression(numbers, required_ops[:]) # copy required_ops because list is mutable
      try:
        with Timeout():
          result = parse_expr(solution).simplify()
          if result.is_integer and TARGET_RANGE[0] <= result <= TARGET_RANGE[1]:
            target = int(result)
            break
      except: continue
    if target is None: continue

    numbers.sort()
    print(numbers)
    print(f'Target: {target}')
    while True:
      user_input = input('Expression: ')
      if user_input in ['q','quit']: print(f'Solution: {solution}'); sys.exit()
      try:
        user_numbers = sorted([int(s) for s in user_input.replace('(',' ').replace(')',' ').replace('+',' ').replace('-',' ').replace('*',' ').replace('/',' ').replace('%',' ').split() if s.isdigit()]) # replace symbols with spaces to isolate digits
        if user_numbers != numbers: print(f'Wrong numbers. Used {user_numbers}, needed {numbers}'); continue
        with Timeout(): diff = (parse_expr(user_input) - target).simplify()
        if diff == 0: print('Correct!'); break
        print(f'Incorrect (got {user_input}, want {target})')
      except Exception as e: print(f'Error: {e}')