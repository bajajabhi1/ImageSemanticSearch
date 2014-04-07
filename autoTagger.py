import os, subprocess, random, shutil, cPickle as cp
#from pymatbridge import Matlab

"""
This script should automate the process of tagging images using the matlab
code.
The functions that are needed are as follows-
loader - returns a list of all filenames that need to be processed
randomizer - randomly permutes the loaded files (so that the data-set is not biased)
tagger - makes a call to the getBiconcept.exe file

"""
print os.getcwd()
print "AutoTagger Loaded"


photopath = os.path.join(os.getcwd(),'photos_HL')

def loader(rootpath=photopath):
  """
  Returns the full list of files + paths in the corpus
  """
  fullist =[]
  for path, subdirs, files in os.walk(rootpath):
    for name in files:
      if '.json' not in name:
        #print path, name
        curpath = os.path.join(path,name)
        fullist += [curpath]
  return fullist


def store(processed, randomlist):
  f = open("queue.dat",'w')
  cp.dump((randomlist,processed),f)
  print "file store complete"
  f.close()
  return

def load():
  f = open("queue.dat",'r')
  randomlist, processed = cp.load(f)
  print "File load complete"
  f.close()
  return randomlist, processed

testpath = '..\\binary\\test.jpg'

def calltagger(pathToPic=testpath):
  print "calltagger invoked"
  #pathToTagger= os.path.join(os.getcwd(),'getBiconcept')
  pathToTagger = 'getBiconcept'
  print pathToTagger
  print pathToPic
  try:
    cmd = 'getBiconcept ' + pathToPic
    process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode

  except Exception as e:
    print dir(e)
    print e.message
    print e.output
    print "Error happened"
  #print poutput
  print out
  print err
  retcode = None
  #retcode = subprocess.call ("getBiconcept "+pathToPic, shell=True)
  #retcode = subprocess.call([pathToTagger,pathToPic])
  return retcode

def process_queue(processed,randomlist):
  try:
    print "Processing queue"
    print processed, len(randomlist)
    while(processed<len(randomlist)):
      fileToProcess = randomlist[processed+1]
      print "Processing ",fileToProcess
      path,filename = os.path.split(fileToProcess)
      binary_path = os.path.join(os.getcwd())
      shutil.copy(fileToProcess,binary_path)
      #filename = os.path.join(binary_path, filename)
      print "File copied to root"
      retcode = calltagger(filename)
      print retcode
      os.remove(filename)
      print "File cleaned/deleted"
      if retcode == 0:
        processed+=1
        print "No. of files processed: ", (processed + 1)
        store(processed, randomlist)
      else:
        print "failure at file no:",processed
        processed+=1 
    return processed
  except Exception as e:
    print e.message
    return processed


def main():
  try:
    lst, processed = load()
  except:
    lst = loader(photopath)
    print len(lst), "elements loaded"
    processed = -1
    random.shuffle(lst)
    store(processed,lst)
  print "processed",processed
  print "list: ",lst
  #try
  if True:
    processed = process_queue(processed,lst)
    store(processed,lst)
  #except Exception as e:
  #store (processed,lst)
  #raise (e)
  print "Graceful exit"
  return 

"""
def mat_calltagger(mlab, pathToPic=testpath):
  print "Matlab calltagger invoked"
  print "Testpath,", pathToPic
  pathToTagger = os.path.join(os.getcwd(),'source') 
  pathToTagger= 'getBiconcept'
  retcode = subprocess.call([pathToTagger,pathToPic])
  return retcode

def mat_process_queue(processed,randomlist, mlab):
  try:
    print "Processing queue"
    while(processed<len(randomlist)):
      fileToProcess = randomlist[processed+1]
      print "Processing ",fileToProcess
      path,filename = os.path.split(fileToProcess)
      shutil.copy(fileToProcess,'.')
      print "File copied to root"
      retcode = mat_calltagger(mlab,filename)
      os.remove(filename)
      print "File cleaned/deleted"
      if retcode == 0:
        processed+=1
        print "No. of files processed: ", (processed + 1)
        store(processed, randomlist)
      else:
        print "failure at file no:",processed
        processed+=1 
    return processed
  except:
    return processed


def mat_main():
  # Initialise MATLAB
  mlab = Matlab(port=4000)
  # Start the server
  mlab.start()
  try:
    lst, processed = load()
  except:
    lst = loader(photopath)
    print len(lst), "elements loaded"
    processed = -1
    random.shuffle(lst)
    store(processed,lst)
  print "processed",processed
  print "list: ",lst[processed:processed+10]
  try:
    processed = mat_process_queue(processed,lst,mlab)
    store(processed,lst)
  except:
    print "Exception happened"
    store (processed,lst)
  
  # Run a test function: just adds 1 to the argument a
  """
"""
  for i in range(10):
    print mlab.run('~/Sites/python-matlab-bridge/test.m', {'a': i})['result']
  """
"""
  # Stop the MATLAB server
  mlab.stop()
  print "Shutdown matlab- Gracefully exiting"
  return 
"""
if __name__ == "__main__":
   main()
