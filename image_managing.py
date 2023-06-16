from PIL import Image
import numpy as np
import math
from utils import imodule, coprime
import sys
#from watermark_embedding_extraction import LSB

#Return numpy array from a Image file
def loadImage(path=""):
    if path == "":
        sys.exit("LOAD IMAGE: Path must not be None!")

    img = Image.open(path)
    return img

#Show image from array or path
def showImage(img):
    if type(img) != str:
        img.show()
    else:
        if img == "":
            sys.exit("SHOW IMAGE: Path must not be None!")
        Image.open(img).show()

#Save image from array or Image file
def saveImage(img, path):
    if path == "":
        sys.exit("SHOW IMAGE: Path must not be None!")
    img.save(path)

def grayscale(img):
    return img.convert(mode="L")

#Return binarized image
def binarization(img):
    return img.convert(mode="1",dither=0)

#Return image size
def imgSize(img):
    if type(img) == np.ndarray:
        width, heigth = (img.shape[1], img.shape[0])
    else:
        width, heigth = img.size
    return width, heigth

#Arnold transform
def arnoldTransform(img, iteration):
    width, heigth = imgSize(img)
    if width != heigth:
        sys.exit("ARNOLD TRANSFORM: Image must be square!")
    side = width
    toTransform = img.copy()
    transformed = img.copy()
    
    for iter in range(iteration):
        
        for i in range(side):
            for j in range(side):
                newX = (i + j) % side
                newY = (i + 2*j) % side
                value = toTransform.getpixel(xy=(i,j))
                transformed.putpixel(xy=(newX,newY),value=value)  
        toTransform = transformed.copy()

    return transformed


#Inverse Arnold transform
def iarnoldTransform(img, iteration):
    width, heigth = imgSize(img)
    if width != heigth:
        sys.exit("IARNOLD TRANSFORM: Image must be square!")
    side = width
    transformed = img.copy()
    toTransform = img.copy()
    
    for iter in range(iteration):
        
        for i in range(side):
            for j in range(side):
                newX = (2*i - j) % side
                newY = (-i + j) % side
                value = toTransform.getpixel(xy=(i,j))
                transformed.putpixel(xy=(newX,newY),value=value)  
        toTransform = transformed.copy()
    return transformed

#2D lower triangular mapping
def lowerTriangularMappingTransform(img, iteration, c, a=-1, d=-1):
    width, heigth = imgSize(img)
    coprime_mode = "first"
    if a == -1 and d == -1:
        a = coprime(width, coprime_mode)
        d = coprime(heigth, coprime_mode)
    
    transformed = img.copy()
    toTransform = img.copy()
    
    for iter in range(iteration):
        
        for i in range(width):
            for j in range(heigth):
                newX = (a*i) % width
                newY = (c*i + d*j) % heigth
                value = toTransform.getpixel(xy=(i,j))
                transformed.putpixel(xy=(newX,newY),value=value)  

        toTransform = transformed.copy()
    
    return transformed
    
#2D inverse lower triangular mapping
def ilowerTriangularMappingTransform(img, iteration, c, a=-1, d=-1):
    width, heigth = imgSize(img)
    coprime_mode = "first"
    if a == -1 and d == -1:
        a = coprime(width, coprime_mode)
        d = coprime(heigth, coprime_mode)
    
    transformed = img.copy()
    toTransform = img.copy()
    ia = imodule(a, width)
    id = imodule(d, heigth)
    for iter in range(iteration):
        
        for i in range(width):
            for j in range(heigth):
                newX = (ia*i) % width
                newY = (id*(j + (math.ceil(c*width/heigth)*heigth) - (c*newX))) % heigth
                value = toTransform.getpixel(xy=(i,j))
                transformed.putpixel(xy=(newX,newY),value=value)  

        toTransform = transformed.copy()
    return transformed

#2D upper triangular mapping
def upperTriangularMappingTransform(img, iteration, c, a=-1, d=-1):
    width, heigth = imgSize(img)
    coprime_mode = "first"
    if a == -1 and d == -1:
        a = coprime(width, coprime_mode)
        d = coprime(heigth, coprime_mode)
    
    transformed = img.copy()
    toTransform = img.copy()
    
    for iter in range(iteration):
        
        for i in range(width):
            for j in range(heigth):
                newX = (a*i + c*j) % width
                newY = (d*j) % heigth
                value = toTransform.getpixel(xy=(i,j))
                transformed.putpixel(xy=(newX,newY),value=value)  

        toTransform = transformed.copy()
    
    return transformed
    
#2D inverse upper triangular mapping
def iupperTriangularMappingTransform(img, iteration, c, a=-1, d=-1):
    width, heigth = imgSize(img)
    coprime_mode = "first"
    if a == -1 and d == -1:
        a = coprime(width, coprime_mode)
        d = coprime(heigth, coprime_mode)
    
    transformed = img.copy()
    toTransform = img.copy()
    ia = imodule(a, width)
    id = imodule(d, heigth)
    for iter in range(iteration):
        
        for i in range(width):
            for j in range(heigth):
                newY = (id*j) % heigth
                newX = (ia*(i + (math.ceil(c*heigth/width)*width) - (c*newY))) % width
                value = toTransform.getpixel(xy=(i,j))
                transformed.putpixel(xy=(newX,newY),value=value)  

        toTransform = transformed.copy()
    return transformed

def mappingTransform(mode, img, iteration, c, a=-1, d=-1):
    if mode == "lower":
        m = lowerTriangularMappingTransform(img,iteration,c,a,d)
        return m
    if mode == "upper":
        m = upperTriangularMappingTransform(img,iteration,c,a,d)
        return m
    else:
        sys.exit("MAPPING TRANSFORM: Mode must be lower or upper!")

def imappingTransform(mode, img, iteration, c, a=-1, d=-1):
    if mode == "lower":
        m = ilowerTriangularMappingTransform(img,iteration,c,a,d)
        return m
    if mode == "upper":
        m = iupperTriangularMappingTransform(img,iteration,c,a,d)
        return m
    else:
        sys.exit("MAPPING TRANSFORM: Mode must be lower or upper!")

'''
TESTING
'''
if __name__ == "__main__":
    img = loadImage("right.png")
    imgr = loadImage("07.jpg")
    imgr = binarization(imgr)
    
    """
    t = arnoldTransform(img,iteration=1)
    showImage(t)

    it = iarnoldTransform(t,iteration=1)
    showImage(it)

    m = mappingTransform(mode="lower",img=imgr,iteration=1,c=3,a=5)
    showImage(m)
    #saveImage(m, "triangular_2_iterations.png")

    im = imappingTransform(mode="lower",img=m,iteration=1,c=3,a=5)
    showImage(im)

    m1 = mappingTransform(mode="upper",img=imgr,iteration=1,c=3)
    showImage(m1)
    #saveImage(m, "triangular_2_iterations.png")

    im1 = imappingTransform(mode="upper",img=m1,iteration=1,c=3)
    showImage(im1)
    """