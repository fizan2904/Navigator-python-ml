import Algorithmia
import base64
import math
from PIL import Image


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
infile = "test/two.jpg"
outfile = "test/out2.jpg"
line = find_horizon(infile)
print "Left Coordinates : "
print line['left']
print "Right Coordinates : "
print line['right']
rotation = calculate_rotation(line)
print rotation
rotate_image(infile, outfile, -rotation, True)