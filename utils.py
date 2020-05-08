import numpy as np
import matplotlib.pyplot as plt
import cv2

def pre_process(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h,w = img.shape
    h = h - h%5
    w = w - w%5
    img = img[0:h,0:w]
    
    return img

def get_tile(img, i, j):
    tile = img[i:i+5, j:j+5]
    return tile

def tile_operations():
    
    b11 = [[0,0],[0,1],[0,2],[0,3]]
    b12 = [[0,1],[0,2],[0,3]]
    
    b21 = [[0,4],[1,4],[2,4],[3,4]]
    b22 = [[1,4],[2,4],[3,4]]
    
    b31 = [[4,1],[4,2],[4,3],[4,4]]
    b32 = [[4,1],[4,2],[4,3]]
    
    b41 = [[1,0],[2,0],[3,0],[4,0]]
    b42 = [[1,0],[2,0],[3,0]]
    
    p1 = []
    p2 = []
    
    ## top-left corner
    for x2,y2 in b21:
        p1.append([0,0])
        p2.append([x2,y2])
    for x2,y2 in b31:
        p1.append([0,0])
        p2.append([x2,y2])
    p1.append([0,0])
    p2.append([4,0])
        
    ## left column
    for x1,y1 in b12:
        for x2,y2 in b22:
            p1.append([x1, y1])
            p2.append([x2, y2])
        for x2,y2 in b31:
            p1.append([x1, y1])
            p2.append([x2, y2])
        for x2,y2 in b41:
            p1.append([x1, y1])
            p2.append([x2, y2])
    
    ## bottom-left corner
    for x2,y2 in b31:
        p1.append([0,4])
        p2.append([x2,y2])
    for x2,y2 in b41:
        p1.append([0,4])
        p2.append([x2,y2])
    
    ## bottom row
    for x1,y1 in b22:
        for x2,y2 in b32:
            p1.append([x1, y1])
            p2.append([x2, y2])
        for x2,y2 in b41:
            p1.append([x1, y1])
            p2.append([x2, y2])
    
    ## bottom-right corner
    for x2,y2 in b41:
        p1.append([4,4])
        p2.append([x2,y2])
    
    ## right column
    for x1,y1 in b32:
        for x2,y2 in b42:
            p1.append([x1, y1])
            p2.append([x2, y2])
    
    return p1,p2
