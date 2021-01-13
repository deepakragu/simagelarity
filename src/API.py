"""
API Code to calculate how similar two images are
Author: Deepak Ragu
"""
from PIL import Image                                                                                
import requests
from io import BytesIO
import imagehash
import os



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
   return readFilenameMethod1(filename)
   


"""
Given two images, calculates how similar the images are
Input: Image1, Image2 (two image objects)
Output: Double (Similarity, as a percentage)
"""
def similarity(image1, image2):
   return similarityMethod1(image1, image2)
   




def readURLMethod1(url):
   response = requests.get(url)
   img = Image.open(BytesIO(response.content))
   return img

def readFilenameMethod1(filename):
   cwd = os.getcwd()
   filepath = cwd + '/images/sample_images/' + filename #ToDo: Make sure to change the directory for this line to user_images
   return Image.open(filepath) 

def similarityMethod1(image1, image2):
   hash = imagehash.average_hash(image1)
   otherhash = imagehash.average_hash(image2)
   image1.show() 
   image2.show() 
   return hash - otherhash