import API
import Authentication
import re
import json


import flask
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

"""
Main Method: Runs all other methods in this file and in other classes
"""
@app.route('/similarity', methods=['GET'])
def main():
    parameters = request.args
    # print(parameters)
    # print(request.query_string)
    API_key = parameters.get('key')
    image1_link = parameters.get('image1')
    image2_link = parameters.get('image2')
    try:
        s = calc_sim(API_key, image1_link, image2_link)
        if (s == None):
            s = "none"
    except Exception as inst:
        s = str(inst)
    return s
        # return "<h1>S(Image)larity</h1><p>===========================================================================</p><p>Hello User! Welcome to SImageLarity, a simple API that calculates the similarity level of two images!</p><p>"+ s +"</p>"

    
    


def run_app():
    app.run()

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


    



"""
Shutfown server if invalid credentials
"""
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

"""
If users would like to use API from command line and using input.txt files
"""
def textual_runner():

    ready_to_use = input("\nTo get started, make sure you have filled out input.txt. Press (y) when you are ready to continue: ")
    while (ready_to_use != "y"):
        print("\nPlease make sure to enter the \'y\' character on your keyboard.")
        ready_to_use = input("Press (y) when you are ready to continue: ")
    API_key, image1_link, image2_link = read_input_file()
    return calc_sim(API_key, image1_link, image2_link)
    
    
"""
Method used to validate API Key and calculate similarity
"""    
def calc_sim(API_key, image1_link, image2_link):
    try:
        

        print("\nChecking Credentials ...")
        valid = Authentication.validate_credentials(API_key)
        if (not valid):
            raise Exception("Invalid credentials. Please check to make sure you have a valid API key")


        print("\nValid Credentials! Calculating similarity of images ... ")
        # print(image1_link)
        # print(image2_link)
        API_Call = json.loads(API.runner(image1_link, image2_link))


        percent = API_Call["similarity"]
        print("\nThe two images are " + str(percent) + "% similar!")
        if (percent < 30):
            print("Guess these images don't look so similar after all!")
        elif (percent < 60):
            print("I can sort of see the resemblance ...")
        else:
            print("Wow! These two are hard to tell apart!")


        print("===========================================================================")


        return API_Call

    except Exception as inst:
        print(inst.args)
        return







"""
Reads and parses file labelled "input.txt" and returns API_Key and image filenames/urls
Input: n/a
Output: API_key, image1_link, image2_link
"""
def read_input_file():

    f = open("input.txt", "r")
    cred = f.readline()
    link1 = f.readline()
    link2 = f.readline()


    try:
        API_key = re.search('API Key: *(.+)', cred).group(1)
        image1_link = re.search('Image 1: *(.+)', link1).group(1)
        image2_link = re.search('Image 2: *(.+)', link2).group(1)
    except AttributeError:
        raise Exception("Error in parsing input.txt file. Please make sure input.txt is properly formatted")

    return API_key, image1_link, image2_link





    

    





