"""
API Code to calculate how similar two images are
Author: Deepak Ragu
"""
import json

from PIL import Image                                                                                
import requests
from io import BytesIO
import imagehash
import os
import cv2

from skimage import measure

import matplotlib.pyplot as plt
import numpy as np




"""
Reads an image url into an image object (Example image URL: https://static.toiimg.com/photo/72975551.cms)
Input: url of image on internet
Output: image object
"""
def readImageURL(url):
   return readURLMethod1(url)



"""
Reads an image file into an image object
Input: local filname of image
Output: image object
"""
def readImageFilename(filename):
   return readFilenameMethod2(filename)
   


"""
Given two images, calculates how similar the images are
Input: Image1, Image2 (two image objects)
Output: Double (Similarity, as a percentage)
"""
def similarity(image1, image2):
   first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
   second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

   img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
   print(img_hist_diff)
   img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
   img_template_diff = abs(img_template_probability_match)
   print(img_template_diff)

   # Taking weighted sum of the two methods
   commutative_image_diff = 0.3 * img_hist_diff + 0.7 * img_template_diff
   
   percent = int(commutative_image_diff * 100)

   data = {"similarity": percent}
   json_object = json.dumps(data)   
   return json_object
   








def readURLMethod1(url):
   response = requests.get(url)
   img = Image.open(BytesIO(response.content))
   return img

"""
For regular filepath and PIL images to be used with imagehash
"""
def readFilenameMethod1(filename):
   cwd = os.getcwd()
   filepath = cwd + '/images/sample_images/' + filename #ToDo: Make sure to change the directory for this line to user_images
   return Image.open(filepath) 

"""
Regular imagehash method
"""
def similarityMethod1(image1, image2):
   hash = imagehash.average_hash(image1)
   otherhash = imagehash.average_hash(image2)
   # image1.show() 
   # image2.show() 
   return hash - otherhash



"""
For OpenCV Images
"""
def readURLMethod1(url):
   response = requests.get(url)
   img = Image.open(BytesIO(response.content))
   return img


"""
For OpenCV images
"""
def readFilenameMethod2(filename):
   cwd = os.getcwd()
   filepath = cwd + '/images/sample_images/' + filename #ToDo: Make sure to change the directory for this line to user_images
   img = cv2.imread(filepath, 0)
   return img

"""
OpenCV + histogram technique
"""
def similarityMethod2(image_1, image_2):
   



















def readURLMethod3(url):
   response = requests.get(url)
   img = Image.open(BytesIO(response.content))
   return img

"""
OpenCV read with SSIM and MSE
"""
def readFilenameMethod3(filename):
   cwd = os.getcwd()
   filepath = cwd + '/images/sample_images/' + filename #ToDo: Make sure to change the directory for this line to user_images
   img = cv2.imread(filepath)
   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   return img


"""
OpenCV with MSE and SSIM method
"""
def similarityMethod3(original, contrast):
   return compare_images(original, contrast)


def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
def compare_images(imageA, imageB):
	# compute the mean squared error and structural similarity
	# index for the images
	# m = mse(imageA, imageB)
	s = measure.compare_ssim(imageA, imageB)
	return int(s*100)
   











"""
For OpenCV images
"""
def readFilenameMethod4(filename):
   cwd = os.getcwd()
   filepath = cwd + '/images/sample_images/' + filename #ToDo: Make sure to change the directory for this line to user_images
   img = cv2.imread(filepath, 0)
   return img

"""
OpenCV technique
"""
def similarityMethod4(image_1, image_2):
   sift = cv2.xfeatures2d.SIFT_create()
   kp_1, desc_1 = sift.detectAndCompute(image_1, None)
   kp_2, desc_2 = sift.detectAndCompute(image_2, None)
   index_params = dict(algorithm=0, trees=5)
   search_params = dict()
   flann = cv2.FlannBasedMatcher(index_params, search_params)
   matches = flann.knnMatch(desc_1, desc_2, k=2)
   good_points = []
   ratio = 0.6 # If you decrease the ratio value, for example to 0.1 you will get really high quality matches, but the downside is that you will get only few matches.
   for m, n in matches:
      if m.distance < ratio*n.distance:
         good_points.append(m)
         # print(len(good_points))
   result = cv2.drawMatches(image_1, kp_1, image_2, kp_2, good_points, None)
   number_keypoints = 0
   if len(kp_1) <= len(kp_2):
      number_keypoints = len(kp_1)
   else:
      number_keypoints = len(kp_2)
   # print("Keypoints 1ST Image: " + str(len(kp_1)))
   # print("Keypoints 2ND Image: " + str(len(kp_2)))
   return (len(good_points) / number_keypoints) * 100


















