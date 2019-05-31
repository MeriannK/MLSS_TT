from PIL import Image
import argparse
import glob

ap = argparse.ArgumentParser()
ap.add_argument("--path", "-dev_dataset", required = True, help = "path to input dataset of images")
args = vars(ap.parse_args())

class Hash(object):

    def __init__(self, image):
        self.image = image

    def ahash(self):
        im = self.image
        size = 24, 24
        im = im.resize(size, Image.ANTIALIAS)
        im = im.convert('L')
        pixels = list(im.getdata())
        average = sum(pixels) / len(pixels)

        result = ''
        for pixel in pixels:
            if pixel > average:
                result += '1'
            else:
                result += '0'
                
        return result
    
def hamming_distance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


images = []

for imagePath in glob.glob(args['path'] + "/*.jpg"):
    images.append(imagePath)

tuples = [(x,y) for x in sorted(images) for y in sorted(images) if x != y]
for entry in tuples:
    if (entry[1], entry[0]) in tuples:
        tuples.remove((entry[1],entry[0]))

for pair in tuples:
    
    first_image = Image.open(pair[0])
    first_image_hasher = Hash(first_image)
    first_image_score = first_image_hasher.ahash()

    second_image = Image.open(pair[1])
    second_image_hasher = Hash(second_image)
    second_image_score = second_image_hasher.ahash()
    
    diff = hamming_distance(first_image_score, second_image_score)
    if diff == 0:
        print("Duplicate: {} and {}".format(pair[0].split('/', 2)[-1], pair[1].split('/', 2)[-1]))
    elif diff > 0 and diff < 55:
        print("Modification: {} and {}".format(pair[0].split('/', 2)[-1], pair[1].split('/', 2)[-1]))
    elif diff > 55 and diff < 125:
        print("Similar: {} and {}".format(pair[0].split('/', 2)[-1], pair[1].split('/', 2)[-1]))
        

