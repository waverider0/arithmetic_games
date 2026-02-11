#!/usr/bin/env python3
import math, random, ast, sys

# Settings
OPS = ['+', '-', '*', '/', '**']
TARGET_RANGE = [10, 400]
NUMBER_RANGE = [2, 20] # Kept small to make mental math reasonable
NUMBER_COUNT = 5

class Node:
    def __init__(self, val=None, op=None, left=None, right=None):
        self.val = val     # The evaluated result of this node
        self.op = op       # Operator string (None for leaves)
        self.left = left   # Left child Node
        self.right = right # Right child Node

    def is_leaf(self):
        return self.left is None

    def __str__(self):
        if self.is_leaf(): return str(self.val)
        return f"({self.left} {self.op} {self.right})"

def catalan_split(n):
    """Returns a split index based on Catalan distribution."""
    if n == 1: return 0
    def nCr(n, r): return math.comb(n, r)
    def cat(k): return nCr(2*k, k) // (k+1)
    
    weights = [cat(k - 1) * cat(n - k) for k in range(1, n)]
    return random.choices(range(1, n), weights=weights)[0]

def generate_skeleton(n):
    """Generates a random tree shape with operators, but NO values."""
    if n == 1:
        return Node() # Placeholder leaf
    
    split = catalan_split(n)
    left = generate_skeleton(split)
    right = generate_skeleton(n - split)
    op = random.choice(OPS)
    return Node(op=op, left=left, right=right)

def force_value(node, target):
    """
    Recursively modifies a subtree to equate to 'target'.
    Returns True if successful, False if mathematically impossible/out of bounds.
    """
    if node.is_leaf():
        if NUMBER_RANGE[0] <= target <= NUMBER_RANGE[1]:
            node.val = int(target)
            return True
        return False

    # Attempt to solve equation for one child, keeping the other fixed
    # We prefer modifying the simpler/shallower child, or the one connected by +/-
    
    # Try modifying Left: target = NewLeft op Right
    req_l = None
    if node.op == '+': req_l = target - node.right.val
    elif node.op == '-': req_l = target + node.right.val
    elif node.op == '*': 
        if node.right.val != 0 and target % node.right.val == 0:
            req_l = target // node.right.val
    elif node.op == '/': req_l = target * node.right.val
    
    if req_l is not None:
        if force_value(node.left, req_l):
            node.val = target # Update cache
            return True

    # Try modifying Right: target = Left op NewRight
    req_r = None
    if node.op == '+': req_r = target - node.left.val
    elif node.op == '-': req_r = node.left.val - target   # L - R = T => R = L - T
    elif node.op == '*': 
        if node.left.val != 0 and target % node.left.val == 0:
            req_r = target // node.left.val
    elif node.op == '/': 
        # L / R = T => R = L / T. strict division check.
        if target != 0 and node.left.val % target == 0:
            req_r = node.left.val // target
    
    if req_r is not None:
        if force_value(node.right, req_r):
            node.val = target
            return True

    return False

def evaluate_and_repair(node):
    """
    Post-order traversal. Evaluates nodes. 
    If an operator constraint is violated, attempts to repair children.
    """
    # 1. Base Case: Leaves get random numbers
    if node.is_leaf():
        node.val = random.randint(*NUMBER_RANGE)
        return

    # 2. Recurse
    evaluate_and_repair(node.left)
    evaluate_and_repair(node.right)

    # 3. Apply Operator & Check Constraints
    l, r, op = node.left.val, node.right.val, node.op
    
    valid = False
    
    # --- Constraint Checking & Repair Logic ---
    
    # Division: Strict Integer Division required
    if op == '/':
        if r != 0 and l % r == 0: 
            valid = True
        else:
            # Fix it: Force Left to be a multiple of Right
            # Find closest multiple to keep numbers reasonably small
            multiplier = max(1, l // r) if r != 0 else 1
            target_l = r * multiplier
            if force_value(node.left, target_l):
                valid = True
            elif r != 0:
                # Alternate fix: Force Right to be a divisor of Left
                # This is harder, let's just try to force Left to result=1 (L=R)
                if force_value(node.left, r):
                    valid = True

    # Power: Magnitude check
    elif op == '**':
        if -5 <= r <= 5 and abs(l) < 20: # Keep powers tiny
             # Check for imaginary/huge results
             try:
                 res = l ** r
                 if isinstance(res, complex) or abs(res) > 2000: valid = False
                 else: valid = True
             except: valid = False
        
        if not valid:
            # Fixing powers is hard, usually easier to swap op
            pass 

    # Multiplication: Magnitude check for playability
    elif op == '*':
        if abs(l * r) <= 2000: valid = True
        else:
            # Try to shrink one operand
            pass # Implicitly falls through to swap

    else: # + and - are usually always fine 
        valid = True

    # 4. Final Fallback: Swap Operator
    # If the randomly chosen operator (e.g. / or **) couldn't be satisfied 
    # even after trying to force values, degrade to + or - or *
    if not valid:
        # Prefer * if small, then -, then +
        if abs(l * r) < 1000: node.op = '*'
        else: node.op = random.choice(['+', '-'])
    
    # 5. Execute (guaranteed valid now)
    ops_func = {
        '+': lambda a,b: a+b,
        '-': lambda a,b: a-b,
        '*': lambda a,b: a*b,
        '/': lambda a,b: a//b,
        '**': lambda a,b: int(a**b)
    }
    node.val = ops_func[node.op](node.left.val, node.right.val)

def extract_leaves(node):
    if node.is_leaf(): return [node.val]
    return extract_leaves(node.left) + extract_leaves(node.right)

def generate_puzzle():
    # Retry loop is now just for Target Range, not structural validity.
    # The generation inside is P-Time (linear to N)
    for _ in range(100): 
        root = generate_skeleton(NUMBER_COUNT)
        evaluate_and_repair(root)
        
        if TARGET_RANGE[0] <= root.val <= TARGET_RANGE[1]:
            return extract_leaves(root), root.val, str(root)
    return None

if __name__ == '__main__':
    result = generate_puzzle()
    if result:
        nums, target, soln = result
        print(f"Numbers: {sorted(nums)}")
        print(f"Target:  {target}")
        
        # Obfuscate solution for interaction
        user_in = input("Expression ('q' for answer): ")
        if user_in.strip() == 'q':
            print(f"Solution: {soln}")
        else:
            try:
                # Basic validation using eval (safe in this constrained env)
                if eval(user_in) == target:
                    print("Correct!")
                else: 
                    print(f"Incorrect. Result was {eval(user_in)}")
            except:
                print("Invalid expression.")
