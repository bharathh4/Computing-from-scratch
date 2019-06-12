def gate(x, y):
    return y if x == 0 else 0

def _not(x):
    return gate(x, y=1)

def _pass(x):
    return _not(_not(x))

def _and(x, y):
    return gate(_not(x), y)

def _or(x, y):
    return _not(gate(x, _not(y)))

def _xor(x, y):
    return _or(gate(x, _pass(y)), gate(_not(x), _not(y)))
    #return gate(x, _not)

def _if(x, y):
    return _not(_xor(x, y))

def _vanilla_add(x, y):

    def _sum(x, y):
        return _xor(x, y)
    
    def _carry_out(x, y):
        return _and(x, y)
    
    return (_carry_out(x, y), _sum(x, y))

def _generalized_add(x, y, carry_in):

    def _sum(x, y, carry_in):
        return _or(gate(_if(carry_in, 0), _not(_xor(x, y))), gate(_not(_if(carry_in, 0)),  _xor(x, y)))

    def _carry_out(x, y, carry_in):
        return _or(gate(_if(carry_in, 0), _or(x, y)), gate(_not(_if(carry_in, 0)), _and(x, y)))

    return _carry_out(x, y, carry_in), _sum(x, y, carry_in)

def eight_bit_add(x1, x2, x3, x4, x5, x6, x7, x8, 
                  y1, y2, y3, y4, y5, y6, y7, y8):
    c1, s1 = _generalized_add(x1, y1, 0)
    c2, s2 = _generalized_add(x2, y2, c1)
    c3, s3 = _generalized_add(x3, y3, c2)
    c4, s4 = _generalized_add(x4, y4, c3)
    c5, s5 = _generalized_add(x5, y5, c4)
    c6, s6 = _generalized_add(x6, y6, c5)
    c7, s7 = _generalized_add(x7, y7, c6)
    c8, s8 = _generalized_add(x8, y8, c7)

    return s8, s7, s6, s5, s4, s3, s2, s1

def space():
    return 79 * '#'


if __name__ == "__main__":
    
    items = [_not(1), 
            _not(0),
            _pass(1),
            _pass(0),
            space(),
            _and(0, 0), _and(0, 1), _and(1, 0), _and(1, 1),
            space(),
            _or(0, 0), _or(0, 1), _or(1, 0), _or(1, 1),
            space(),
            _xor(0, 0), _xor(0, 1), _xor(1, 0), _xor(1, 1),
            space(),
            _if(0, 0), _if(0, 1), _if(1, 0), _if(1, 1),
            space(),
            _vanilla_add(0, 0), _vanilla_add(0, 1), _vanilla_add(1, 0), _vanilla_add(1, 1),
            space(),
            _generalized_add(0, 0, 0), _generalized_add(0, 1, 0), _generalized_add(1, 0, 0), _generalized_add(1, 1, 0), 
            _generalized_add(0, 0, 1), _generalized_add(0, 1, 1), _generalized_add(1, 0, 1), _generalized_add(1, 1, 1),
            eight_bit_add(1, 1, 0, 0, 0, 0, 0, 0, 
                          1, 0, 0, 0, 0, 0, 0, 0)
    ]

    for item in items:
        print(item)

# vanilla add
'''
x y cout s
0 0 0 0
0 1 0 1
1 0 0 1
1 1 1 0
'''

# generalized add
'''
x y cin cout s
0 0  0   0   0
0 0  1   0   1
0 1  0   0   1
0 1  1   1   0
1 0  0   0   1
1 0  1   1   0
1 1  0   1   0
1 1  1   1   1
'''

