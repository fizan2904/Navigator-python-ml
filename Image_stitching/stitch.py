from panorama import Stitcher
import argparse
import imutils
import cv2
from matplotlib import pyplot as plt
import Algorithmia
import base64
import math
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required = True, help = "Path to the first image")
ap.add_argument("-s", "--second", required = True, help = "Path to the second image")
args = vars(ap.parse_args())

def find_horizon(infile):
    algo = client.algo('ukyvision/deephorizon/0.1.0')
    image = base64.b64encode(open(infile, "rb").read())
    return algo.pipe({'image':'data:image/jpg;base64,'+image}).result


def calculate_rotation(coords):
    (x1, y1) = coords['left']
    (x2, y2) = coords['right']
    slope = (y2-y1)/(x2-x1)
    return math.degrees(math.atan(slope))


def rotate_image(infile, outfile, degrees, crop):
    Image.open(infile).rotate(degrees, expand=not crop, resample=Image.BILINEAR).save(outfile)

client = Algorithmia.client('simVPnwkWmla6+BAakyvCoAhfnH1')
infile = "images/left.jpg"
outfile = "images/left1.jpg"
line = find_horizon(infile)
print "Left Coordinates for left file: "
print line['left']
print "Right Coordinates for left file: "
print line['right']
rotation = calculate_rotation(line)
print rotation
rotate_image(infile, outfile, -rotation, True)

infile1 = "images/right.jpg"
outfile1 = "images/right1.jpg"
line1 = find_horizon(infile1)
print "Left Coordinates for right file: "
print line['left']
print "Right Coordinates for right file: "
print line['right']
rotation1 = calculate_rotation(line1)
print rotation
rotate_image(infile1, outfile1, -rotation1, True)

imageA = cv2.imread(outfile)
imageB = cv2.imread(outfile1)
imageA = imutils.resize(imageA, width = 400)
imageB = imutils.resize(imageB, width = 400)

stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches = True)
edges = cv2.Canny(result, 100, 200)

cv2.imshow("Image A", imageA)
cv2.imshow("Image B", imageB)
cv2.imshow("Key point matches", vis)
cv2.imshow("Result", result)
cv2.imshow("Edge", edges)
cv2.waitKey(0)