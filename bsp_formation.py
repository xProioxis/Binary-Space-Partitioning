class Segment:
    
    vector = None

    def __init__(self, label, x1, y1, x2, y2):
        self.label = label
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.vector = (x2-x1, y2-y1)
        self.norm_vec = (self.vector[1], -self.vector[0])
        self.midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)


def cross_product(vec1, vec2):
    result =  (vec1[0] * vec2[1]) - (vec1[1] * vec2[0])
    return result

def dot_product(vec1, vec2):
    print((vec1[0] * vec2[0]) + (vec1[1] * vec2[1]))
    return (vec1[0] * vec2[0]) + (vec1[1] * vec2[1])

segs = [
    Segment("A", 0, 0, 0, 100),
    Segment("B", 0, 100, 100, 100),
    Segment("C", 100, 100, 100, 0),
    Segment("D", 100, 0, 0, 0),
    Segment("H", 70, 50, 80, 40),
    Segment("G", 80, 40, 90, 50),
    Segment("F", 90, 50, 80, 60),
    Segment("E", 80, 60, 70, 50)
]


H = segs[4]

for seg in segs:

    
    to_midpoint = (seg.midpoint[0] - H.x1, seg.midpoint[1] - H.y1)

    if dot_product(H.norm_vec, to_midpoint) < 0:
        print(f"{seg.label} is on the left of H")
    else:
        print(f"{seg.label} is on the right of H")