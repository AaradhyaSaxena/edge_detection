import numpy as np
import matplotlib.pyplot as plt
import cv2

## crops for 5x5 tiles
def pre_process(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h,w = img.shape
    h = h - h%5
    w = w - w%5
    img = img[0:h,0:w]
    
    return img

## slice of image
def get_tile(img, i, j):
    tile = img[i:i+5, j:j+5]
    return tile

## returns co-ords of points at the boundary of tiles
## at the lower-most level
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

## To be computed using Bicubic interpolation, trapezoidal rule later
## returns integration of intensities of pixels from p1 to p2
def integrate(img, x1,y1, x2,y2): 
    incr = 0
    totalPix = 0
    intensity=0
    if y2 > y1:
        yincr = 1
    else:
        yincr = -1
    if x2 > x1:
        xincr = 1
    else:
        xincr = -1
    if (abs(y2-y1) > abs(x2-x1)):
        x = x1
        ## To handle the case where Den is zero
        if(x2==x1):
            yPerx = 0
        else:
            yPerx = round(abs(y2-y1)/abs(x2-x1))
        count = 0
        y = y1
        while(y < y2):
            intensity += img[x,y]
            count += 1
            
            if count == yPerx:
                x = x + xincr
                count = 0
            totalPix += 1
            y += yincr
    else:
        y = y1
        ## To handle the case where Den is zero
        if(y2==y1):
            xPery = 0
        else:
            xPery = round(abs(x2-x1)/abs(y2-y1))
        count = 0
        x = x1
        while(x < x2):
            
            intensity += img[x,y]
            count += 1
            
            if count == xPery:
                y = y+ yincr
                count = 0
            totalPix +=1
            x += xincr
    if(totalPix==0):
        return 0
    return intensity/totalPix

## check against segmentation fault
def insideImage(x1,y1,x2,y2,h=125,w=125):
    if(x1<0 or x1>=w or x2<0 or x2>=w or y1<0 or y1>=h or y2<0 or y2>=h):
        return 0
    return 1

## computes L-infinite between 2 points
def computeL(x1,y1,x2,y2):
    if(not insideImage(x1,y1,x2,y2)):
        return 0
    return max(abs(x1 - x2), abs(y1 - y2))

## returns integration of intensities of pixels from p1 to p2 divided by l(p1,p2)
def meanIntensityStLine(img, x1,y1,x2,y2):
    if(not insideImage(x1,y1,x2,y2)):
        return 0
    l = computeL(x1,y1,x2,y2)
    if l ==0:
        return 0
    return integrate(img, x1,y1, x2,y2) / l

# def meanIntensityCurve(L1,F1, L2,F2):
#     return ((L1*F1 + L2*F2)/(L1+L2))

## checks if the points are on adjacent sides or oppo side
## to choose between llgm and trap.d
def onOppositeSide(x1,y1,x2,y2):
    if(abs(x1-x2)== 4 or abs(y1-y2)==4):
        return 1
    else:
        return 0
    
def horzToVert(x1,y1,x2,y2):
    if(x2==x1):
        return 0
    if((y2-y1)/(x2-x1)<0):
        return 1
    else:
        return 0
    
## returns response between 2 given points
def tileResponse(img, x1,y1,x2,y2):
    side = horzToVert(x1,y1,x2,y2)
    if(onOppositeSide(x1,y1,x2,y2) != 0):
        return parallelogramResp(img, x1,y1,x2,y2, side)
    else:
        return quadrilateralResp(img, x1,y1,x2,y2, side)
    
## returns the llgm response between 2 given points
def parallelogramResp(img, x1,y1,x2,y2, side):
    sum1 = 0
    sum2 = 0
    w = 2
    if side ==0:
        s = 1
        while(s <= (w)/2):
            sum1 += (computeL(x1+s, y1, x2+s, y2))* meanIntensityStLine(img, x1+s,y1,x2+s,y2) - (computeL(x1, y1-s, x2, y2-s))* meanIntensityStLine(img, x1,y1-s,x2,y2-s)
            sum2 += computeL(x1+s, y1, x2+s, y2) - computeL(x1-s, y1, x2-s, y2)
            s += 1
    else:
        s = 1
        while(s <= (w)/2):
            sum1 += (computeL(x1, y1+s, x2, y2+s))* meanIntensityStLine(img, x1,y1+s,x2,y2+s) - (computeL(x1, y1-s, x2, y2-s))* meanIntensityStLine(img, x1,y1-s,x2,y2-s)
            sum2 += computeL(x1, y1+s, x2, y2+s) - computeL(x1, y1-s, x2, y2-s)
            s += 1
    
    if sum2==0:
        return 0
    else:
        return abs(sum1/sum2)

## returns the trap.d response between 2 given points
def quadrilateralResp(img, x1,y1,x2,y2, side):
    sum1 = 0
    sum2 = 0
    w = 2
    if side ==0:
        s = 1
        while(s <= (w)/2):
            sum1 += (computeL(x1+s, y1, x2, y2+s))* meanIntensityStLine(img, x1+s,y1,x2,y2+s) - (computeL(x1-s, y1, x2, y2-s))* meanIntensityStLine(img, x1-s,y1,x2,y2-s)
            sum2 += computeL(x1+s, y1, x2, y2+s) - computeL(x1-s, y1, x2, y2-s)
            s += 1
    else:
        s = 1
        while(s <= (w)/2):
            sum1 += (computeL(x1, y1+s, x2+s, y2))* meanIntensityStLine(img, x1,y1+s,x2+s,y2) - (computeL(x1, y1-s, x2-s, y2))* meanIntensityStLine(img, x1,y1-s,x2-s,y2)
            sum2 += computeL(x1, y1+s, x2+s, y2) - computeL(x1, y1-s, x2-s, y2)
            s += 1
            
    if sum2==0:
        return 0
    else:
        return abs(sum1/sum2)

## returns response corresponding to (xi, yi)
def initialize_beam_curve(img):
    p1i = []
    p2i = []
    ri = []
    h,w = img.shape

    p1,p2 = tile_operations()
    i = 0
    while(i<h-4):
        j = 0
        row = []
        while(j<w-4):
            p1_temp = list(np.asarray(p1) + [i,j])
            p2_temp = list(np.asarray(p2) + [i,j])
            
            p1i.append(p1_temp)
            p2i.append(p2_temp)
            
            for k in range(len(p1_temp)):
                x1,y1 = p1_temp[k]
                x2,y2 = p2_temp[k]
                row.append(tileResponse(im,x1,y1,x2,y2))
            j += 5
            
        ri.append(row)
        i += 5

    return p1i, p2i, ri


def bottom_most_level_(img,p1i,p2i):
    response = []
    for i in range(len(p1i)):
        for j in range(len(p1i[i])):
            x1,y1 = p1i[i][j]
            x2,y2 = p2i[i][j]
            res = tileResponse(img,x1,y1,x2,y2)
            response.append(res)
    return response

# returns threshold
def threshold(x1,y1,x2,y2):
    L = computeL(x1,y1,x2,y2)
    alpha = 4
    complexity = 15
    w = 2
    sigma = 0.1
    beta = complexity*2-1
    w = 2*w
    T = sigma*np.sqrt(2*(np.log(6*res.N)+0*(beta*L/alpha)*log(2))/(w*L))  
    return T




















