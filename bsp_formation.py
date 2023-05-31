from Segment import Segment

def cross_product(vec1, vec2):
    #print((vec1[0] * vec2[1]) - (vec1[1] * vec2[0]))
    return  (vec1[0] * vec2[1]) - (vec1[1] * vec2[0])

def dot_product(vec1, vec2):
    return (vec1[0] * vec2[0]) + (vec1[1] * vec2[1])

def euclid_distance(p1, p2):
    return ( (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 )**(1/2)

def within_seg(seg, inter_x, inter_y):
    within_x = min(seg.x1, seg.x2) <= inter_x <= max(seg.x1, seg.x2)
    within_y = min(seg.y1, seg.y2) <= inter_y <= max(seg.y1, seg.y2)
    return within_x and within_y
    

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
        print(node.segment.label, end=" ")# print(node.segment.label, f"({node.segment.x1},{node.segment.y1}), ({node.segment.x2},{node.segment.y2}) ({node.segment.vector[0]},{node.segment.vector[1]})", end=" ")
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

    def show_tree_help(self, node, adjust=30):
        if node == None:
            return ""
        if node.left == None and node.right == None:
            return node.segment.label
        
        pad = ""
        for i in range(adjust):
            pad += " "

        connection = " ".join((pad, "|    |"))

        print(node.segment.label)
        print(connection)
        print( " ".join((pad[:-5], self.show_tree_help(node.left, adjust-1))), " ".join((pad + "    ", self.show_tree_help(node.right, adjust + 1))) )

    def show_tree(self):
        self.show_tree_help(self.root)
        


def make_bsp(node, seg_list):
    
    # this function splits the scene into left and right halves, then recusively creates a binary space partition tree
    #print(f"========{node.segment.label}========")
    #for seg in seg_list:
    #        print(seg.label, f"({seg.x1},{seg.y1}) ({seg.x2},{seg.y2})", end = " ")
    #print()
    #print(f"====================================")

    curr_seg = node.segment
    if len(seg_list) == 0:
        return
    
    left = list()
    right = list()

    
    if not curr_seg.is_wall and 2 <= len(seg_list):

        
        curr_distance = None

        f_nearest_wall = None
        f_nearest_wall_dis = float("inf")
        f_intersect_x = f_intersect_y = 0

        b_nearest_wall = None
        b_nearest_wall_dis = float("inf")
        b_intersect_x = b_intersect_y = 0

        for seg in seg_list:
            if seg.is_wall:
                # front splitting
                updated = False

                # initialize the A and B matrix, we need to find x matrix (will allow us to find intersection of two vectors)
                # A = [a_1, a_2]  B = [b1]    x = [t]
                #     [a_3, a_4]      [b2]        [s]
                # Ax = B <==> x = A^(-1)B
                # A^(-1) =  1/(a1*a4 - a2*a3)  *  [a4, -a2]
                #                                 [-a3, a1]
                a1 = seg.vector[0]; a2 = -curr_seg.vector[0]
                a3 = seg.vector[1]; a4 = -curr_seg.vector[1]
                b1 = curr_seg.x1 - seg.x1
                b2 = curr_seg.y1 - seg.y1
                inv_denom = (a1*a4) - (a2*a3)
                if inv_denom == 0: # no intersection
                    continue
                
                # find intersection points
                t = ((a4 * b1) + (-a2 * b2)) * (1/inv_denom)
                #s = ((-a3 * b1) + (a1 * b2)) * (1/inv_denom)
                intersect_x = seg.x1 + (seg.vector[0] * t)
                intersect_y = seg.y1 + (seg.vector[1] * t)

                # see if this wall is closest so far
                curr_distance = euclid_distance((curr_seg.x1, curr_seg.y1), (intersect_x, intersect_y))
                if curr_distance < f_nearest_wall_dis and within_seg(seg, intersect_x, intersect_y):
                    updated = True
                    f_nearest_wall_dis = curr_distance
                    f_nearest_wall = seg
                    f_intersect_x = intersect_x
                    f_intersect_y = intersect_y

                if not updated: # canot have the same segment be both back and front split
                    # back splitting
                    a1 = seg.vector[0]; a2 = curr_seg.vector[0]
                    a3 = seg.vector[1]; a4 = curr_seg.vector[1]
                    b1 = curr_seg.x1 - seg.x1
                    b2 = curr_seg.y1 - seg.y1
                    inv_denom = (a1*a4) - (a2*a3)
                    if inv_denom == 0: # no intersection
                        continue
                    
                    # find intersection points
                    t = ((a4 * b1) + (-a2 * b2)) * (1/inv_denom)
                    #s = ((-a3 * b1) + (a1 * b2)) * (1/inv_denom)
                    intersect_x = seg.x1 + (seg.vector[0] * t)
                    intersect_y = seg.y1 + (seg.vector[1] * t)

                    # see if this wall is closest so far
                    curr_distance = euclid_distance((curr_seg.x1, curr_seg.y1), (intersect_x, intersect_y))
                    if curr_distance < b_nearest_wall_dis and within_seg(seg, intersect_x, intersect_y):
                        b_nearest_wall_dis = curr_distance
                        b_nearest_wall = seg
                        b_intersect_x = intersect_x
                        b_intersect_y = intersect_y

        #print(f_nearest_wall, b_nearest_wall)
        # for a split to occur, we must have back and front split
        if f_nearest_wall is not b_nearest_wall:
            if f_nearest_wall is not None:
                # split front
                new_final_x = new_init_x = f_intersect_x
                new_final_y = new_init_y = f_intersect_y
                new_first_vec = (f_intersect_x - f_nearest_wall.x1, f_intersect_y - f_nearest_wall.y1)
                #new_second_vec = (f_nearest_wall.x2 - new_init_x, f_nearest_wall.y2 - new_init_y)

                # make appropriate label
                if len(f_nearest_wall.label) == 1:
                    first_new_lbl = f_nearest_wall.label + "1"
                    second_new_lbl = f_nearest_wall.label + "2"
                else:
                    print("activated")
                    num = ""
                    i = len(f_nearest_wall.label) - 1
                    while f_nearest_wall.label[i].isnumeric():
                        num += f_nearest_wall.label[i]
                        i -= 1

                    first_new_lbl = f_nearest_wall.label
                    second_new_lbl = f_nearest_wall.label + f"{int(num) + 1}"
                
                # add new vector to list
                new_wall = Segment(second_new_lbl, new_init_x, new_init_y, f_nearest_wall.x2, f_nearest_wall.y2, True)
                seg_list.append(new_wall)

                # update first half of new vector (will overwrite current vectors place)
                f_nearest_wall.x2 = new_final_x
                f_nearest_wall.y2 = new_final_y
                f_nearest_wall.vector = new_first_vec
                f_nearest_wall.label = first_new_lbl
                f_nearest_wall.norm_vec = (f_nearest_wall.vector[1], -f_nearest_wall.vector[0])
                f_nearest_wall.midpoint = ((f_nearest_wall.x1 + f_nearest_wall.x2) / 2, (f_nearest_wall.y1 + f_nearest_wall.y2) / 2)

            if b_nearest_wall is not None:
                # split back
                new_final_x = new_init_x = b_intersect_x
                new_final_y = new_init_y = b_intersect_y
                new_first_vec = (b_intersect_x - b_nearest_wall.x1, b_intersect_y - b_nearest_wall.y1)
                #new_second_vec = (b_nearest_wall.x2 - new_init_x, b_nearest_wall.y2 - new_init_y)

                # make appropriate label
                if len(b_nearest_wall.label) == 1:
                    first_new_lbl = b_nearest_wall.label + "1"
                    second_new_lbl = b_nearest_wall.label + "2"
                else:
                    num = ""
                    i = len(b_nearest_wall.label) - 1
                    while b_nearest_wall.label[i].isnumeric():
                        num += b_nearest_wall.label[i]
                        i -= 1

                    first_new_lbl = b_nearest_wall.label
                    second_new_lbl = b_nearest_wall.label + f"{int(num) + 1}"
                
                # add new vector to list
                new_wall = Segment(second_new_lbl, new_init_x, new_init_y, b_nearest_wall.x2, b_nearest_wall.y2, True)
                seg_list.append(new_wall)

                # update first half of new vector (will overwrite current vectors place)
                b_nearest_wall.x2 = new_final_x
                b_nearest_wall.y2 = new_final_y
                b_nearest_wall.vector = new_first_vec
                b_nearest_wall.label = first_new_lbl
                b_nearest_wall.norm_vec = (b_nearest_wall.vector[1], -b_nearest_wall.vector[0])
                b_nearest_wall.midpoint = ((b_nearest_wall.x1 + b_nearest_wall.x2) / 2, (b_nearest_wall.y1 + b_nearest_wall.y2) / 2)



        #for seg in seg_list:
        #    print(seg.label, end = " ") #  print(seg.label, seg.x1, seg.y1, seg.x1, seg.y2, end = " ")
        print()
            

            
 
    for seg in seg_list:

        to_init_vector = (seg.x1 - curr_seg.x1, seg.y1 - curr_seg.y1)

        curr_cross_prod = cross_product(to_init_vector, curr_seg.vector)
        if curr_cross_prod < 0:
            left.append(seg)
        elif 0 < curr_cross_prod:
            right.append(seg)
        else: # if initial point of seg and terminal point of curr_seg are the same
            if cross_product(seg.vector, curr_seg.vector) < 0:
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
print("Post Order: ", end="") 
tree.post_order()
print()
print("In Order:   ", end="")
tree.in_order()

#tree.show_tree()


'''
# initialize the A and B matrix, we need to find x matrix (will allow us to find intersection of two vectors)
# A = [a1, a2]  B = [b1]    x = [t]
#     [a3, a4]      [b2]        [s]
# Ax = B <==> x = A^(-1)B
# A^(-1) =  1/(a1*a4 - a2*a3)  *  [a4, -a2]
#                                 [-a3, a1]
curr_seg = segs[2]
seg = segs[1]

a1 = seg.vector[0]; a2 = curr_seg.vector[0]
a3 = seg.vector[1]; a4 = curr_seg.vector[1]
b1 = curr_seg.x1 - seg.x1
b2 = curr_seg.y1 - seg.y1
inv_denom = (a1*a4) - (a2*a3)
if inv_denom == 0: # no intersection
    print("no intersection")

# find intersection points
t = ((a4 * b1) + (-a2 * b2)) * (1/inv_denom)
s = ((-a3 * b1) + (a1 * b2)) * (1/inv_denom)
intersect_x = seg.x1 + (seg.vector[0] * t)
intersect_y = seg.y1 + (seg.vector[1] * t)

# see if this wall is closest so far
curr_distance = euclid_distance((curr_seg.x1, curr_seg.y1), (intersect_x, intersect_y))
print(curr_distance, inv_denom, intersect_x, intersect_y)
'''
    
'''
H = segs[4]


for seg in segs:  
    to_init_vector = (seg.x1 - H.x1, seg.y1 - H.y1)
    if cross_product(to_init_vector, H.vector) < 0:
        print(f"{seg.label} is on the left of H")
    else:
        print(f"{seg.label} is on the right of H")
        '''