#!/usr/bin/env python3
import math, random, sys, time
from collections import Counter
import matplotlib.pyplot as plt

# --- Constraint Settings ---
OPS = ['+', '-', '*', '/', '**']
TARGET_RANGE = [200, 400]
NUMBER_RANGE = [6, 100]
NUMBER_COUNT = 8
SAMPLE_SIZE = 10000

class Node:
    def __init__(self, val=None, op=None, left=None, right=None, is_leaf=False):
        self.val = val
        self.op = op
        self.left = left
        self.right = right
        self.is_leaf = is_leaf

def generate_skeleton(n):
    """Generates a random binary operator tree structure."""
    if n == 1: return Node(is_leaf=True)
    
    # Catalan-ish split
    if n == 2: split = 1
    else: split = random.randint(1, n-1) 
    
    return Node(op=random.choice(OPS), 
                left=generate_skeleton(split), 
                right=generate_skeleton(n - split))

def evaluate_and_repair(node):
    """
    Bottom-up traversal. 
    1. Evaluates L and R.
    2. Checks if (L op R) is valid.
    3. If invalid, FORCES L or R to be different to make it valid.
    """
    # 1. Base Case: Leaves
    if node.is_leaf:
        node.val = random.randint(*NUMBER_RANGE)
        return node.val

    # 2. Recurse (Post-Order)
    l_val = evaluate_and_repair(node.left)
    r_val = evaluate_and_repair(node.right)

    # 3. Constraint Solving
    op = node.op
    
    # --- DIVISION LOGIC ---
    if op == '/':
        # Constraint: L % R == 0.
        # Fix 1: If R is 0, make it 1.
        if r_val == 0: 
            r_val = 1
            node.right.val = 1
            
        # Fix 2: If L % R != 0, change L to be (R * random_multiplier)
        if l_val % r_val != 0:
            # We want the result to be somewhat small, e.g., result <= 20
            desired_result = random.randint(1, 10)
            l_val = r_val * desired_result
            node.left.val = l_val # Force the child node
            
    # --- POWER LOGIC ---
    elif op == '**':
        # Constraint: Result must be < 10^6 and not complex.
        # Heuristic: Base > 1, Exponent usually small.
        
        # Force Base to be small if Exponent is large
        if abs(r_val) > 4:
            r_val = random.randint(2, 4) # Force exponent down
            node.right.val = r_val
            
        if abs(l_val) > 10:
            l_val = random.randint(2, 5) # Force base down
            node.left.val = l_val

        # Safety check: if it's still gonna blow up, swap op
        try:
            res = l_val ** r_val
            if isinstance(res, complex) or abs(res) > 200000:
                op = '+' # Fallback
                node.op = '+'
        except:
            op = '+'
            node.op = '+'

    # 4. Final Evaluation
    try:
        if op == '+': res = l_val + r_val
        elif op == '-': res = l_val - r_val
        elif op == '*': res = l_val * r_val
        elif op == '/': res = l_val // r_val
        elif op == '**': res = int(l_val ** r_val)
    except:
        res = 0 # Default failure case

    node.val = res
    return res

def collect_stats(node, ops_counter, leaves_counter):
    if node.is_leaf:
        leaves_counter[node.val] += 1
    else:
        ops_counter[node.op] += 1
        collect_stats(node.left, ops_counter, leaves_counter)
        collect_stats(node.right, ops_counter, leaves_counter)

def run_test():
    print(f"Generating {SAMPLE_SIZE} valid puzzles...")
    
    ops_counts = Counter()
    leaves_counts = Counter()
    valid_targets = []
    
    generated = 0
    attempts = 0
    
    start_time = time.time()

    # Loop until we have enough SAMPLES
    while generated < SAMPLE_SIZE:
        attempts += 1
        
        # 1. Generate Tree
        root = generate_skeleton(NUMBER_COUNT)
        
        # 2. Force Integers without backtracking
        res = evaluate_and_repair(root)
        
        # 3. Check if result is in Target Range
        if TARGET_RANGE[0] <= res <= TARGET_RANGE[1]:
            collect_stats(root, ops_counts, leaves_counts)
            valid_targets.append(res)
            generated += 1
            
            if generated % 1000 == 0:
                print(f"  {generated}/{SAMPLE_SIZE}...")
        
        # Circuit breaker if we are just failing endlessly
        if attempts > SAMPLE_SIZE * 50:
            print("Error: Rejection rate too high. Adjust constraints.")
            break

    print(f"Finished. Total Attempts: {attempts}. Success Rate: {generated/attempts:.1%}")
    print(f"Time: {time.time() - start_time:.2f}s")
    
    # --- PLOTTING ---
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # 1. Operators
    ops_labels = ops_counts.keys()
    ops_values = ops_counts.values()
    ax1.bar(ops_labels, ops_values, color='skyblue')
    ax1.set_title('Operator Usage')
    
    # 2. Leaves (Numbers used)
    # Filter specific range for cleaner plot
    leaf_vals = sorted(leaves_counts.items())
    x_leaf, y_leaf = zip(*leaf_vals)
    ax2.plot(x_leaf, y_leaf, color='green', alpha=0.7)
    ax2.fill_between(x_leaf, y_leaf, color='green', alpha=0.3)
    ax2.set_title('Leaf Value Frequency')
    ax2.set_xlim(NUMBER_RANGE)
    
    # 3. Targets
    ax3.hist(valid_targets, bins=30, color='orange', alpha=0.7)
    ax3.set_title('Final Target Value Distribution')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_test()
