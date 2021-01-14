import API
import Authentication
import re
import json



"""
Main Method: Runs all other methods in this file and in other classes
"""
def main():
    print("===========================================================================")
    print("Hello User! Welcome to SImageLarity, a simple API that calculates the similarity level of two images!")
    ready_to_use = input("\nTo get started, make sure you have filled out input.txt. Press (y) when you are ready to continue: ")
    while (ready_to_use != "y"):
        print("\nPlease make sure to enter the \'y\' character on your keyboard.")
        ready_to_use = input("Press (y) when you are ready to continue: ")
    
    
    try:
        API_key, image1_link, image2_link = read_input_file()

        print("\nChecking Credentials ...")
        valid = Authentication.validate_credentials(API_key)
        if (not valid):
            raise Exception("Invalid credentials. Please check to make sure you have a valid API key")


        print("\nValid Credentials! Calculating similarity of images ... ")
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


        return

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





    

    





