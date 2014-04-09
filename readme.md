This master branch is deprecated - all active development is on sourceversion - we should probably replace the 2.

> <b>Anj:</b>

How to run the code:
- Put all of these files in /binary/ folder of the matlab code
-   <b>$ python webserver.py </b>
- ^instantiates server running on localhost:8080/upload
- doing a post request to localhost:8080/upload will start the tagging and should return a wellformed JSON.
- doing a get request opens up a simple GUI that should let you upload files and run the full code (for test purposes)
- It's pretty iffy on my computer - the mexFile issues are very irritating.
