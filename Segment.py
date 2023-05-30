class Segment:
    
    vector = None
    visited = False
    is_wall = False

    def __init__(self, label, x1, y1, x2, y2, is_wall=False):
        self.label = label
        self.is_wall = is_wall
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.vector = (x2-x1, y2-y1)
        self.norm_vec = (self.vector[1], -self.vector[0])
        self.midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)