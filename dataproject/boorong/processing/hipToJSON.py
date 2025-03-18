

jsonDict={
  "id": "boo",
  "name": "Boorong",
  "region": "Australia",
  "source": ["Stellarium"],
  "description": "constellations of boorong",
  "constellations": []
}



# id, string name, list of lines
def makeConstellation(id:str,consNames:dict,lines:list):

    con = {

      "id": id,

      "names": [consNames],
    # keep in lists
      "lines": lines
    #   lines is a list of lists of names of stars

    }
    return con





constellationFormat={

      "id": "",

      "names": [{"english": "Andromeda"}],
    # keep in lists
      "lines": [["* alf And", "* del And", "* bet And", "* gam01 And"], ["* omi And", "* iot And", "* kap And", "* lam And"], ["* iot And", "* sig And", "* pi. And", "* del And"], ["* pi. And", "* bet And", "* mu. And", "* nu. And", "* phi And", "* ups Per"], ["* del And", "* eps And", "* zet And", "* eta And"]],

}





##############################

# load star names into dict
consNameDict={}

consNameFile="consNames.txt"

# Open the file in read mode
with open(consNameFile, 'r') as file:
    # Read each line in the file
    for line in file:
        # Print each line
        linelist=line.strip().split("\t")
        for i in range(len(linelist)):
            linelist[i]=linelist[i].strip("\"_()")
        # print(linelist)

        id,nativeName,enName = linelist
        
        consNameDict[id]={"english": enName, "native": nativeName}
        

# print(consNameDict)

#############################################
# load identifyers

starIdentifyers={}

import numpy as np
hipIDs, identities = np.loadtxt("boorong_cords.txt",usecols=(2,3),delimiter='|',unpack=True,dtype=str)


for i in range(len(identities)):
    starIdentifyers[hipIDs[i].strip()]=identities[i].strip()

print(starIdentifyers)
# exit()
##############################################
# make jsonDict

consStarsFile="hipnumbers.txt"
# Open the file in read mode
with open(consStarsFile, 'r') as file:
    # Read each line in the file
    for line in file:
        # Print each line
        consFileList=line.strip().split(" ")
        consID=consFileList[0]
        hipIDlist=consFileList[2:]

        if consID not in consNameDict.keys():
            consNames={"english":"","native":""}
        else:
            consNames = consNameDict[consID]

        print(consID)
        # print(consFileList)
        # print(hipIDlist)
        # print(len(hipIDlist))

        hipListLengh=len(hipIDlist)

        if hipListLengh %2 ==1:
            print("odd")
            raise Exception("non paired hip id list")
        

        

        
        consLines=[]
        consIdentifyerList=[]

        for i in range(hipListLengh//2):
            
            pair=hipIDlist[i:i+2]
            print(pair)
            consLines.append(pair)
            identifyerpair = [starIdentifyers[f"HIP{starID}"] for starID in pair]


            print(identifyerpair)
            consIdentifyerList.append(identifyerpair)
            print(consIdentifyerList)




        


        consEntry= makeConstellation(consID,consNames,consIdentifyerList)
        jsonDict["constellations"].append(consEntry)


import json



outfile="boorong.json"
with open(outfile, 'w') as file:
    file.write(json.dumps(jsonDict, indent=4))