from sympy.ntheory.primetest import isprime 
from itertools import combinations, permutations
import numpy as np
import json

# four blocks total
# which faces hidden for each block
# constraints: two blocks with two faces hidden
# two blocks with one face hidden

b_dict = {
            "s": [0, 1, 2, 3, 4, 5],
            "l": [5, 6, 7, 8, 9, 10]
          }

#same adjacency matrix for both cubes
#assuming we pin 5 to 0
# i.e. use idx-5 to get adjacency for high-val cubes
adj = np.array([[0, 1, 1, 1, 1, 0],
               [1, 0, 1, 0, 1, 1],
               [1, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 1],
               [1, 1, 0, 1, 0, 1],
               [0, 1, 1, 1, 1, 0]])

blocks = [b_dict["s"] for i in range(4)] + [b_dict["l"] for j in range(4)]

def n_face(n_faces, n_hid):
    idcs = list(combinations(list(range(n_faces)), n_hid))
    
    masks = np.array([np.ones(n_faces)]*len(idcs))
    
    for r in range(masks.shape[0]):
        pair = idcs[r]
        for idx in pair:
            masks[r][idx] = 0
    
    return masks

def feasible(ways):
    #checks pairs against dictionary 
    #ways will be a 2D list of hidden face values
    #for different selections of four cubes
    #this is specific to covering 1 or 2 faces
    for i in range(len(ways)):
        new_way = []
        for val in ways[i]:
            if len(val) == 1:
                new_way.append(val)
            elif len(val) > 1:
                try:
                    if adj[val[0]][val[1]]:
                        new_way.append(val)
                except IndexError:
                   if adj[val[0]-5][val[1]-5]:
                        new_way.append(val) 
        ways[i] = new_way
    return ways


def get_hid(blocks, n_hid):
    #seems like I could get the hidden faces here
    #blocks will be a three-deep list
    #of lists of ways to select four blocks
    #where each block is a list of faces

    #from this, I want ways to hide sets of faces
    #so n_hid should be a list of #faces/block to hide
    #this will return a list of lists
    size = len(n_hid)

    #this is not generalized: only works for 6-sided shapes
    #example: I need ways to hide 1 and 1 and 2 and 2 faces
    #can just do it in order for each permutation of n_hid
    ways = list(set(permutations(n_hid)))
    all_ways = []
    for block_set in blocks:
        block_sets_ways = []
        for way in ways:
            block_ways = []
            for p in range(len(way)):
                block_ways.append(list(combinations(block_set[p], way[p])))
            block_sets_ways.append(block_ways)
        all_ways.append(block_sets_ways)
    
    return all_ways

def select_blocks(b):
    choices = list(combinations(b, 4))
    sel = []

    for r in choices:
        f = list(r)
        if f in sel:
            pass
        else: 
            sel.append(f)
    
    return sel

#this actually calculates the sum of the faces
#it needs to know how many 
def face_sum():
    return 0

def main():
    
    b = ["s"]*4 + ["l"]*4
    blocks = select_blocks(b)
    
    #sums will later serve as a key to the block options in big
    sums = [sum(np.array([b_dict[k] for k in s]).flatten()) for s in blocks]
    
    big = get_hid([[b_dict[k] for k in s] for s in blocks], [1, 1, 1, 2])
    sep_dict = {sums[i]: big[i] for i in range(len(blocks))}
    sum_dict = {}
    for key in sep_dict.keys():
        #get all combinations
        way = sep_dict[key]
        #way: one way of hiding 1, 1, 2, 2 faces
        #sep_dict[60][0] is 1, 2, 1, 2 for s, s, s, s
        for choice in way:
            combs = []
            # for i in choice for choice in way
            for i in choice[0]:
                for j in choice[1]:
                    for k in choice[2]:
                        for l in choice[3]:
                            out = [i, j, k, l]
                            val = sum([sum(v) for v in out])
                            if isprime(key - val):
                                combs.append([i, j, k, l])
            
            print((combs))
            print("=!"*20)


if __name__ == "__main__":
    main()