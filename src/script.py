import Main

print("===========================================================================")
print("Hello User! Welcome to SImageLarity, a simple API that calculates the similarity level of two images!")

ready_to_use = input("\nTextual input (t) or GET requests (g)? ")
while (ready_to_use != "t" and ready_to_use != "g"):
    print("\nPlease make sure to enter the \'t\' character or the \'g\' character on your keyboard.")
    ready_to_use = input("\nTextual input (t) or GET requests (g)? ")

if (ready_to_use == "t"):
    Main.textual_runner()

if (ready_to_use == "g"):
    print("\nIf you would like to make a GET request, please open a new command prompt and curl your url")
    print("\nThe URL you use to make a get request should formatted as follows: http://127.0.0.1:5000/similarity?key=YOUR_API_KEY&image1=IMAGE_URL_OR_FILENAME&image2=IMAGE_URL_OR_FILENAME")
    print("\nExample GET request: curl \"http://127.0.0.1:5000/similarity?key=6bch723&image1=rose2.jpeg&image2=rose3.jpeg\"")
    print("\nYou may make as many curl requests as you would like")
    print("\nTo Quit, enter control+c in this command prompt")
    print()
    Main.run_app()
