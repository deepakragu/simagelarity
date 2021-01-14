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
    Main.run_app()
    # Main.main()