geometries = {
    (0, 0, 0, 0): {'type': 'flat', 'quad': (0, 1, 2, 3)},
    (0, 0, 0, 1): {'type': 'flat-high', 'tri1': (0, 1, 2), 'tri2': (0, 2, 3)},
    (0, 0, 1, 0): {'type': 'flat-high', 'tri1': (0, 1, 3), 'tri2': (1, 2, 3)},
    (0, 0, 1, 1): {'type': 'slope', 'quad': (0, 1, 2, 3)},
    (0, 1, 0, 0): {'type': 'flat-high', 'tri1': (0, 2, 3), 'tri2': (0, 1, 2)},
    (0, 1, 0, 1): {'type': 'saddle'},
    (0, 1, 1, 0): {'type': 'slope', 'quad': (0, 1, 2, 3)},
    (0, 1, 1, 1): {'type': 'flat-low', 'tri1': (1, 2, 3), 'tri2': (0, 1, 3)},
    (1, 0, 0, 0): {'type': 'flat-high', 'tri1': (1, 2, 3), 'tri2': (0, 1, 3)},
    (1, 0, 0, 1): {'type': 'slope', 'quad': (0, 1, 2, 3)},
    (1, 0, 1, 0): {'type': 'saddle'},
    (1, 0, 1, 1): {'type': 'flat-low', 'tri1': (2, 3, 0), 'tri2': (0, 1, 2)},
    (1, 1, 0, 0): {'type': 'slope', 'quad': (0, 1, 2, 3)},
    (1, 1, 0, 1): {'type': 'flat-low', 'tri1': (0, 1, 3), 'tri2': (1, 2, 3)},
    (1, 1, 1, 0): {'type': 'flat-low', 'tri1': (0, 1, 2), 'tri2': (0, 2, 3)},
}

print(geometries[(1, 0, 0, 0)]['type'])
print(geometries[(1, 0, 0, 0)]['tri1'])

# points for quads are redundant as they are always the full set
