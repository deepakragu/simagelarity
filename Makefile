default:
	$(info ===========================================================================)
	$(info Hello User! Welcome to SImageLarity, a simple API that calculates the similarity level of two images!)
	$(info ===========================================================================)



	@read -p "Textual input (t) or GET requests (g)? " line \
	&&  if [ $${line} = "g" ]; then python3 DyNotify.py; else python3 src/script.py; fi \
	&& echo $${line}


