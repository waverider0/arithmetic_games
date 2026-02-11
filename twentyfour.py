#!/usr/bin/env python3
import ast, math, random, re, readline, signal, sys
from sympy import parse_expr

OPS = ['+', '-', '*', '/', '**']
TARGET_RANGE = [10,400]
NUMBER_RANGE = [2,100]
NUMBER_COUNT = 5

class Timeout:
  def __enter__(self, *a): signal.signal(signal.SIGALRM, self.h); signal.setitimer(signal.ITIMER_REAL, 0.5)
  def __exit__(self, *a): signal.setitimer(signal.ITIMER_REAL, 0)
  def h(self, *a): raise TimeoutError('TLE')

def catalan(n:int): return math.comb(2*n, n) // (n+1)

def generate_expression(nums:list[int], required_ops:list[str]) -> str|None:
  if len(nums) == 1: return str(nums[0])

  n = len(nums) - 1
  weights = [catalan(k - 1) * catalan(n - k) for k in range(1, len(nums))]
  split = random.choices(range(1, len(nums)), weights=weights)[0]
  left = generate_expression(nums[:split], required_ops)
  right = generate_expression(nums[split:], required_ops)
  if (left is None) or (right is None): return None

  op = required_ops.pop() if required_ops else random.choice(OPS)
  expression = f'({left} {op} {right})'
  if op == '**' and (parse_expr(left) > 20 or parse_expr(right) > 10): return None

  with Timeout(): evaluated = parse_expr(expression)
  if not evaluated.is_rational: return None
  if evaluated > 1e6: return None

  return expression

if __name__ == '__main__':
  while True:
    numbers = [random.randint(*NUMBER_RANGE) for _ in range(NUMBER_COUNT)]
    required_ops = [op for op in OPS if random.choice([True, False])]
    random.shuffle(required_ops)
    target = None
    for _ in range(100): # 100 retries
      random.shuffle(numbers)
      solution = generate_expression(numbers, required_ops[:]) # copy required_ops because list is mutable
      if solution == None: continue
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
    user_input = input('Expression: ')
    if user_input == 'q': print(f'Solution: {ast.unparse(ast.parse(solution))}'); sys.exit() # parse then unparse to remove redundant parentheses
    try:
      user_numbers = sorted([int(s) for s in re.split(r'\D+', user_input) if s])
      evaluated_input = parse_expr(user_input)
      if user_numbers != numbers: print(f'Wrong numbers. Used {user_numbers}, needed {numbers}'); continue
      with Timeout(): diff = (evaluated_input - target).simplify()
      if diff == 0: print('Correct!'); break
      print(f'Incorrect (got {evaluated_input}, want {target})')
    except Exception as e: print(f'Error: {e}')