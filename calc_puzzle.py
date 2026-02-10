#!/usr/bin/env python3

import sympy

"""
given a set of primitives and a target value,
construct a definite integral from [0,<a primitive>]
that evaluates to the target value.

e.g:
[x, sin, pi]
Target: -2
Answer: Integral(sin(x), (x, 0, pi))

the example above is a good puzzle because the target value
is "opaque". if the upper bound was instead 2, the target would
be cos(2) - 1 which is less opaque since it gives away the answer.

opacity = (F node count - target node count) / F node count
 0: no simplification
 1: fully simplified

1) generate F and b where F(b)-F(0)=target and opacity(target) >= MIN_OPACITY
2) simplify F, then F'=f
3) simplify f, then extract the primitives
4) parse and evaluate the player's input

* if the player uses every primitive exactly once and forms an expression different than sympy's f'(x) but still evaluates to target, that's fine
* time/resource limit to prevent validation stalls during generation
"""

DEPTH_RANGE = [2,4]
BREADTH_RANGE = [4,8]
MAX_TARGET_NODES = 10
MIN_OPACITY = 0.3

if __name__ == '__main__':
  pass