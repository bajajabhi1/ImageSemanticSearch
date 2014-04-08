import web, os
import json
import time
from conceptExtraction import retrieveResultsAPI


import web

urls = ('/upload', 'Upload')


print "initializing new calltagger"
def calltagger(filename="test.jpg"):
    template = "matlab -nojvm -r \"getBiconcept('{0}'); quit;\"".format(filename)
    print "Tagging ", filename
    rcode = 0
    try:
        rcode=os.system(template)
        time.sleep(5)
    except:
        print "Process start failed"
    return rcode

backendFailure = {"message": "backend failure"}

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
            t1 = time.time()
            print "Invoking autotagger"
            #Damn thing doesn't work, but let's assume it does
            rcode = calltagger(filename)
            out_dict == {};
            while(time.time()-t1<200 and (out_dict=={}
                                     or
                                     out_dict==backendFailure)):    
                out_dict,fpath = retrieveResultsAPI(filename)
                time.sleep(1)
            print "Tagging complete"
            print "Time taken: ", time.time()-t1
            print "final outdict received"
            #rcode
            os.remove(os.path.join(filedir,filename))
            os.remove(fpath)
            print "File removal complete"
            
            #Now I need to access the output, parse it and return it as JSON            
        #raise web.seeother('/upload')
        return json.dumps(out_dict)

if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()



