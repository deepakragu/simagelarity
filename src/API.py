"""
API Code to calculate how similar two images are
Author: Deepak Ragu
"""
import json
import os
import cv2
import numpy as np
import urllib
from validator_collection import validators, checkers, errors





"""
Runs the necessary methods of this API class to produce desired output
Input: URL/Filepaths to images
Output: JSON Object
"""
def runner(image1_link, image2_link):


   print("Comparing", image1_link, "vs.", image2_link)


   image1 = image2 = None
   if (checkers.is_url(image1_link) or checkers.is_ip_address(image1_link)):
      image1 = readImageURL(image1_link)
   else:
      image1 = readImageFilename(image1_link)
   if (checkers.is_url(image2_link) or checkers.is_ip_address(image2_link)):
      image2 = readImageURL(image2_link)
   else:
      image2 = readImageFilename(image2_link)
   if (image1 is None or image2 is None or image1 == [] or image2 == []):
      raise Exception("Invalid Image Link(s). Please check to make sure the provided URL/filename is correct")


   return similarity(image1, image2)
   


"""
Reads an image url into an image object
Input: url of image on internet
Output: image object
"""
def readImageURL(url):
   # download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return image



"""
Reads an image file into an image object
Input: local filname of image
Output: image object
"""
def readImageFilename(filename):
   cwd = os.getcwd()
   filepath = cwd + '/images/user_images/' + filename 
   img = cv2.imread(filepath, 0)
   return img
   


"""
Given two images, calculates how similar the images are
Input: Image1, Image2 (two image objects)
Output: JSON Object containing percentage (can be accessed by accessing "similarity")
"""
def similarity(image_1, image_2):
   first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
   second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

   img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
   img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
   img_template_diff = abs(img_template_probability_match)

   # Taking weighted sum of the two methods
   commutative_image_diff = 0.25 * img_hist_diff + 0.75 * img_template_diff
   
   percent = int(commutative_image_diff * 100)

   data = {"similarity": percent}
   json_object = json.dumps(data)   
   return json_object
   





