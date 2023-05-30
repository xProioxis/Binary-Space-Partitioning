# |--------------------|
# | --                 |
# | --            -----|
# |   .           -   -|
# |               -----|
# |          _         |
# |         /_|        |
# |--------------------|

# Basis for an algorithm going over Binary Space Partitioning

from Segment import Segment

view_pos = (15, 40)
segments = [ Segment("A", 0, 0, 0, 100), Segment("B", 0, 100, 100, 100), Segment("C", 100, 100, 100, 0), Segment("D", 100, 0, 0, 0),
            Segment("E", 10, 60, 20, 60), Segment("F", 20, 80, 10, 80), Segment("G", 10, 60, 10, 80), Segment("H", 20, 60, 20, 80), # box 1
           Segment("I",80, 50, 80, 20), Segment("J", 90, 20, 90, 50), Segment("K", 80, 50, 90, 50), Segment("L", 80, 20, 90, 20)] # box 2
           #Segment((60, 80), (70, 70)], [(60, 80), (70, 80)], [(70, 80), (70, 70)], # triangle 1
           #[(25, 10), (40, 15)], [(25, 10), (40, 10)], [(40, 10), (40, 15)] # triangle 2
           #]





for seg in segments:
    
    in_front = False

    if in_front:
        print(seg, "is in front!")
    else:
        print(seg, "is behind!")