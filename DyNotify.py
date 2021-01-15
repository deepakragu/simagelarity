import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image
from urllib.request import urlopen
from validator_collection import validators, checkers, errors
import imagehash
import re
import json
import os
import cv2
import numpy as np
from skimage.measure import compare_ssim

"""
Usage:
 * Open Command prompt
 * run make
 * Open another Command Prompt
 * run curl "http://localhost:8000/key=YOUR_API_KEY&image1=IMAGE1_URL_OR_FILENAME&image2=IMAGE2_URL_OR_FILENAME"
"""
class DyNotify(BaseHTTPRequestHandler):
    def _read_image_url(self, url):
        # im = Image.open(urlopen(url))
        # return im
        resp = urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image

    def _read_image_filename(self, filename):
        cwd = os.getcwd()
        filepath = cwd + '/' + filename 
        img = cv2.imread(filepath, 0)
        return img

    def _calculate_sim(self, image_1, image_2):
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])
        img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        return int(img_hist_diff * 100)

    def _similarity(self, image1_link, image2_link):
        if (checkers.is_url(image1_link) or checkers.is_ip_address(image1_link)):
            image1 = self._read_image_url(image1_link)
        else:
            image1 = self._read_image_filename(image1_link)
        if (checkers.is_url(image2_link) or checkers.is_ip_address(image2_link)):
            image2 = self._read_image_url(image2_link)
        else:
            image2 = self._read_image_filename(image2_link)
        if (image1 is None or image2 is None):
            raise Exception(f"Invalid Image Link(s). Please check to make sure the provided URL/filename ({image1_link}, {image2_link}) is correct")
            return

        percent = self._calculate_sim(image1, image2)

        data = {"similarity": percent}
        json_object = json.dumps(data)   
        return json_object

    def _validate_credentials(self, API_key):
        credential_format = "kmrhn74zgzcq4nqb"
        if (not re.match(credential_format, API_key)):
            raise Exception("invalid credentials")
        return True

    def _extract_info(self, path):
        try:
            API_key = re.search('key=*(.+)&', path).group(1)
            image1_link = re.search('image1=*(.+)&', path).group(1)
            image2_link = re.search('image2=*(.+)$', path).group(1)
            return API_key, image1_link, image2_link
        except AttributeError:
            raise Exception("Error in parsing input.txt file. Please make sure input.txt is properly formatted")

    def do_GET(self):
        self.send_response(200)
        new_line_str = f"\n"
        self.wfile.write(new_line_str.encode("utf8"))
        try:
            API_key, image1_link, image2_link = self._extract_info(self.path)
            valid_key = self._validate_credentials(API_key)
            self.wfile.write(self._similarity(image1_link, image2_link).encode("utf8"))
        except Exception as inst:
            self.wfile.write(inst.encode("utf8"))
        self.wfile.write(new_line_str.encode("utf8"))
        self.wfile.write(new_line_str.encode("utf8"))
        
def run(server_class=HTTPServer, handler_class=DyNotify, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    run()