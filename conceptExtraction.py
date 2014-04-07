import sys
from itertools import izip
import json
import os

classfilepath = "class1200.txt"
classfile = open(classfilepath,'r')

#scoresfilepath = "brighteyes-biconcept.txt"
#scoresfile = open(scoresfilepath,'r')

def extractConcept(concepts,scores, limit=0.7):
    count = 0
    for line in izip(concepts,scores):
        count+=1
        concept, score = line
        score = float(score)
        if score>limit:
            print concept, score
    return count

def retrieveResultsAPI(filename):
    """
    Open results directory
    """
    resultdir = os.path.join(os.getcwd(),"result")
    results = os.listdir(resultdir)
    head = filename.split('.')[0]
    biconceptfile = head+'-biconcept.txt'
    outDict = {}
    filepath = None
    if biconceptfile in results:
        print "Results discovered"
        filepath = os.path.join(resultdir,biconceptfile)
        resultfile = open(filepath, 'r')
        outlist = extractConceptList(classfile, resultfile)
        if type(outlist) == int:
            print "Something went wrong- filesize mismatch-debug- count", outlist
        else:
            outDict["filename"] = filename
            outDict["features"] = outlist
            #print "Removing resultsfile ", resultfile
            #os.remove(filepath)
            
    return outDict, filepath
    #Remove output file
    
    
def extractConceptList(concepts=classfile, scores=None, limit = 0.0):
    #Takes concept values and parses them into a dictionary
    count = 0
    outlist = []
    for concept, score in izip(concepts,scores):
        count+=1
        outlist+=[{ "id"    :   count,
                    "key"   :   concept.strip(),
                    "value" :   score.strip()    }]
    if count==1200:
        return outlist
    else:
        return count
        
#extractConcept(classfile,scoresfile)


"""
JSON structure
{
    name = " "
    features = [
                {f_id:"1", key: "sunny_day", value: "0.12"},
                {f_id:"2", key: "misty_moon", value: "0.89"},
                //etc...
                ]
}
"""
