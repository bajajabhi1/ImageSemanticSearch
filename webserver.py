import web, os
import autoTagger
import requests
import json
from conceptExtraction import retrieveResultsAPI
from time import time

import web

urls = ('/upload', 'Upload')

class Upload:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """<html><head></head><body>
                <form method="POST" enctype="multipart/form-data" action="">
                <input type="file" name="myfile" />
                <br/>
                <input type="submit" />
                </form>
                </body></html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = os.getcwd() # change this to the directory you want to store the file in.
        web.header('Content-Type', 'application/json')
        out_dict = {"message": "backend failure"}
        if 'myfile' in x: # to check if the file-object is created

            print "old filename:", x.myfile.filename
            filename = os.path.split(x.myfile.filename)[-1]
            print "new filename", filename
            fout = open(os.path.join(filedir,filename),'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            print "Writeout complete";
            fout.close() # closes the file, upload complete.
            t1 = time()
            print "Invoking autotagger"
            #Damn thing doesn't work, but let's assume it does
            rcode = autoTagger.calltagger(filename)
            print "Tagging complete"
            print "Time taken: ", time()-t1
            out_dict = retrieveResultsAPI(filename)
            print "final outdict received"
            #rcode
            os.remove(os.path.join(filedir,filename))
            print "File removal complete"
            
            #Now I need to access the output, parse it and return it as JSON            
        #raise web.seeother('/upload')
        return json.dumps(out_dict)

if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()



def postimg():
    fileobj = open('test.jpg','rb')
    print "Posting image"
    """
    r = requests.post('http://httpbin.org/post',
        data = {'mysubmit':'Go'},
        files = { 'archive':('testfile.jpg', fileobj) })
    """
    r = requests.post('http://localhost:8080/',
        data = {'mysubmit':'Go'},
        files = { 'archive':('testfile.jpg', fileobj) })
    print r
    print r.json()
