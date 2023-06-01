from Segment import Segment
import pygame
import random
import time

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)



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


"""
Segment("G", 50, 40, 60, 50),
    Segment("A", 0, 0, 0, 100, True),
    Segment("E", 50, 60, 40, 50),
    Segment("B", 0, 100, 100, 100, True),
    Segment("F", 60, 50, 50, 60),
    Segment("C", 100, 100, 100, 0, True),
    Segment("D", 100, 0, 0, 0, True),
    Segment("H", 40, 50, 50, 40)""" # initial correct splitting behavior


"""
Segment("G", 50, 40, 60, 50),
    Segment("Z", 20, 0, 20, 40),
    Segment("A", 0, 0, 0, 100, True),
    Segment("E", 50, 60, 40, 50),
    Segment("B", 0, 100, 100, 100, True),
    Segment("F", 60, 50, 50, 60),
    Segment("C", 100, 100, 100, 0, True),
    Segment("D", 100, 0, 0, 0, True),
    Segment("H", 40, 50, 50, 40)
"""# third split fix

"""
view_pos = (250, 90)
Segment("G", 250, 240, 260, 250),
    Segment("A", 100, 0, 100, 500, True),
    Segment("E", 250, 260, 240, 250),
    Segment("B", 100, 500, 500, 500, True),
    Segment("F", 260, 250, 250, 260),
    Segment("C", 500, 500, 500, 0, True),
    Segment("D", 500, 0, 100, 0, True),
    Segment("H", 240, 250, 250, 240)
""" # more balanced tree fix

colors = [RED,GREEN,BLUE,CYAN,MAGENTA,YELLOW,WHITE,ORANGE]

view_pos = (250, 90)

segs = [
    Segment("G", 250, 240, 260, 250),
    Segment("A", 100, 0, 100, 500, True),
    Segment("E", 250, 260, 240, 250),
    Segment("B", 100, 500, 500, 500, True),
    Segment("F", 260, 250, 250, 260),
    Segment("C", 500, 500, 500, 0, True),
    Segment("D", 500, 0, 100, 0, True),
    Segment("H", 240, 250, 250, 240)
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


    def in_order_nums_help(self, node):
        if node == None:
            return
        
        self.in_order_nums_help(node.left)
        print(node.segment.label, f"({node.segment.x1},{node.segment.y1}), ({node.segment.x2},{node.segment.y2}) ({node.segment.vector[0]},{node.segment.vector[1]})", end=" ")
        self.in_order_nums_help(node.right)


    def in_order_nums(self):
        self.in_order_nums_help(self.root)
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
        return
    
    def make_list_help(self, node, seg_list, view_pos):
        if node == None:
            return

        seg = node.segment
        to_view_vec = (view_pos[0]-seg.x1, view_pos[1]-seg.y1)

        if cross_product(to_view_vec, seg.vector) < 0: # left side
            self.make_list_help(node.left, seg_list, view_pos)
            seg_list.append(node.segment)
            self.make_list_help(node.right, seg_list, view_pos)
        else: # right side
            self.make_list_help(node.right, seg_list, view_pos)
            seg_list.append(node.segment)
            self.make_list_help(node.left, seg_list, view_pos)

        
        
        
    
    def make_list(self, view_pos):
        res = list()
        self.make_list_help(self.root, res, view_pos)
        return res
        

    def show_tree(self):
        print(self.show_tree_help(self.root))
        


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
                    #print("activated")
                    num = ""
                    i = len(f_nearest_wall.label) - 1
                    while f_nearest_wall.label[i].isnumeric():
                        num += f_nearest_wall.label[i]
                        i -= 1

                    first_new_lbl = f_nearest_wall.label
                    second_new_lbl = f_nearest_wall.label[:i+1] + f"{int(num) + 1}"
                
                # add new vector to list
                new_color = colors[random.randint(0, len(colors)-1)]
                while new_color == f_nearest_wall.color:
                    new_color = colors[random.randint(0, len(colors)-1)]

                new_wall = Segment(second_new_lbl, new_init_x, new_init_y, f_nearest_wall.x2, f_nearest_wall.y2, True)
                new_wall.color = new_color
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
                    #print("activated")
                    num = ""
                    i = len(b_nearest_wall.label) - 1
                    while b_nearest_wall.label[i].isnumeric():
                        num += b_nearest_wall.label[i]
                        i -= 1

                    first_new_lbl = b_nearest_wall.label
                    second_new_lbl = b_nearest_wall.label[:i+1] + f"{int(num) + 1}"
                
                # add new vector to list
                new_color = colors[random.randint(0, len(colors)-1)]
                while new_color == b_nearest_wall.color:
                    new_color = colors[random.randint(0, len(colors)-1)]

                new_wall = Segment(second_new_lbl, new_init_x, new_init_y, b_nearest_wall.x2, b_nearest_wall.y2, True)
                new_wall.color = new_color
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

    
    
idx = -1
tree = BSP_Tree(BSP_Node(segs[idx], None, None))
segs.pop(idx)
make_bsp(tree.root, segs)

tree.in_order_nums()
print()
print("Post Order: ", end="") 
tree.post_order()
print()
print("In Order:   ", end="")
tree.in_order()

#BSP_list = tree.make_list()

WINDOW = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Binary Space Partitioning")

WINDOW.fill(BLACK)


running = True
while running:
    WINDOW.fill(BLACK)
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

    '''
    node = tree.root
    seg_stack = list()
    while node != None:
        seg = node.segment
        seg_stack.append(seg)
        view_pos = (90, 90)
        to_view_vec = (view_pos[0]-seg.x1, view_pos[1]-seg.y1)
        

        if cross_product(to_view_vec, seg.vector) < 0:
            node = node.left
        else:
            node = node.right

    pygame.draw.circle(WINDOW, WHITE, view_pos, 3, 3)        
    
    # using only current subsector
    for i in reversed(range(len(seg_stack))):
        seg = seg_stack[i]
        pygame.draw.line(WINDOW, seg.color, (seg.x1, seg.y1),(seg.x2, seg.y2), 1)
        pygame.display.update()
        pygame.time.wait(500)
    '''

    
    BSP_list = tree.make_list(view_pos)
    pygame.draw.circle(WINDOW, WHITE, view_pos, 3, 3)
    for seg in BSP_list:
        #print(seg.label, end=" ")
        pygame.draw.line(WINDOW, seg.color, (seg.x1, seg.y1),(seg.x2, seg.y2), 1)
        pygame.display.update()
        pygame.time.wait(500)
    pygame.time.wait(1000) # allow final line to be drawn