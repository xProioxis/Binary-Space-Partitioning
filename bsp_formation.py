from Segment import Segment

def cross_product(vec1, vec2):
    print((vec1[0] * vec2[1]) - (vec1[1] * vec2[0]))
    return  (vec1[0] * vec2[1]) - (vec1[1] * vec2[0])

def dot_product(vec1, vec2):
    return (vec1[0] * vec2[0]) + (vec1[1] * vec2[1])

'''segs = [
    Segment("A", 0, 0, 0, 100),
    Segment("B", 0, 100, 100, 100),
    Segment("C", 100, 100, 100, 0),
    Segment("D", 100, 0, 0, 0),
    Segment("H", 70, 50, 80, 40),
    Segment("G", 80, 40, 90, 50),
    Segment("F", 90, 50, 80, 60),
    Segment("E", 80, 60, 70, 50)
]'''

"""
Segment("A", 0, 0, 0, 100, True),
    Segment("B", 0, 100, 100, 100, True),
    Segment("C", 100, 100, 100, 0, True),
    Segment("D", 100, 0, 0, 0, True),
    Segment("H", 40, 50, 50, 40),
    Segment("G", 50, 40, 60, 50),
    Segment("F", 60, 50, 50, 60),
    Segment("E", 50, 60, 40, 50)""" # original segs

segs = [
    Segment("G", 50, 40, 60, 50),
    Segment("A", 0, 0, 0, 100, True),
    Segment("E", 50, 60, 40, 50),
    Segment("B", 0, 100, 100, 100, True),
    Segment("F", 60, 50, 50, 60),
    Segment("C", 100, 100, 100, 0, True),
    Segment("D", 100, 0, 0, 0, True),
    Segment("H", 40, 50, 50, 40)
]

class BSP_Node:
    
    def __init__(self, segment, left, right):
        self.segment = segment
        self.left = left
        self.right = right

class BSP_Tree:
    root = None
    def __init__(self, root):
        self.root = root

    def in_order_help(self, node):
        if node == None:
            return
        
        self.in_order_help(node.left)
        print(node.segment.label, end=" ")
        self.in_order_help(node.right)


    def in_order(self):
        self.in_order_help(self.root)
        print()

    def post_order_help(self, node):
        if node == None:
            return
        
        self.post_order_help(node.left)
        self.post_order_help(node.right)
        print(node.segment.label, end=" ")

    def post_order(self):
        self.post_order_help(self.root)
        


def make_bsp(node, seg_list):
    
    # this function splits the scene into left and right halves, then recusively creates a binary space partition tree

    curr_seg = node.segment
    if len(seg_list) == 0:
        return
    
    left = list()
    right = list()

    for seg in seg_list:

        to_init_vector = (seg.x1 - curr_seg.x1, seg.y1 - curr_seg.y1)

        if cross_product(to_init_vector, curr_seg.vector) < 0:
            left.append(seg)
        else:
            right.append(seg)

    if 0 < len(left):
        node.left = BSP_Node(left[0], None, None)
        make_bsp(node.left, left[1:])

    if 0 < len(right):
        node.right = BSP_Node(right[0], None, None)
        make_bsp(node.right, right[1:])

    
    

tree = BSP_Tree(BSP_Node(segs[-1], None, None))
segs.pop(-1)
make_bsp(tree.root, segs)
tree.in_order()
tree.post_order()

    
'''
H = segs[4]


for seg in segs:  
    to_init_vector = (seg.x1 - H.x1, seg.y1 - H.y1)
    if cross_product(to_init_vector, H.vector) < 0:
        print(f"{seg.label} is on the left of H")
    else:
        print(f"{seg.label} is on the right of H")
        '''