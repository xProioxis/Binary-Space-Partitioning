# |--------------------|
# | --                 |
# | --            -----|
# |   .           -   -|
# |               -----|
# |          _         |
# |         /_|        |
# |--------------------|

# Basis for an algorithm going over Binary Space Partitioning

view_pos = (15, 40)
segments = [[(10, 60), (20, 60)], [(10, 80), (20, 80)], [(10, 60), (10, 80)], [(20, 60), (20, 80)], # box 1
           [(80, 50), (80, 20)], [(100, 20), (100, 50)], [(80, 50), (100, 50)], [(80, 20), (100, 20)], # box 2
           [(60, 80), (70, 70)], [(60, 80), (70, 80)], [(70, 80), (70, 70)], # triangle 1
           [(25, 10), (40, 15)], [(25, 10), (40, 10)], [(40, 10), (40, 15)] # triangle 2
           ]




for seg in segments:
    in_front = False
    if seg[0][0] == seg[1][0]: # if purely vertical line
        if view_pos[1] < seg[0][1]: # determine posistion based on y value
            in_front = True
        else:
            in_front = False

    elif seg[0][1] == seg[1][1]: # if purely horizontal line
        if view_pos[1] < seg[0][1]:
            in_front = True
        else:
            in_front = False

    else:
        view_seg_vec = (seg[0][0] - view_pos[0], seg[0][1] - view_pos[1])
        seg_vec = (seg[1][0] - seg[0][0], seg[1][1] - seg[0][1])
        cross_prod = (view_seg_vec[0] * seg_vec[1]) - (view_seg_vec[1] * seg_vec[0])

        if cross_prod < 0:
            in_front = True
        else:
            in_front = False

    if in_front:
        print(seg, "is in front!")
    else:
        print(seg, "is behind!")