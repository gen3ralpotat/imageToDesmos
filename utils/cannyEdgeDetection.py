import numpy as np
import cv2
from PIL import Image
#from matplotlib import pyplot as plt

def image_to_canny_edge_bmp(path: str):
    img = cv2.imread(path, 3)
    edges = cv2.Canny(image=img, threshold1=75, threshold2=500, apertureSize=3, L2gradient=False)

    edgeImage = Image.fromarray(edges)
    edgeImage.save('./output/images/output.bmp')

    #print(f"Saved image to ./output/output.bmp")

    # potrace -s ./output/output.bmp -o ./output/output.svg