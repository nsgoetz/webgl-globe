import string
import pickle

stateResultsFolder= "StateResults/"
simpleResultsFile= "simpleResults.pickle"

stateCodes = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
stateResultsDict = {}

def getParyResFromWeirdStr(s):
    #returns none or (party, pop)
    #can be chnaged later to use the percent but that may mess with merging zones
    A = string.split(s, ';')
    party = A[1]
    if(party != 'GOP' and party != 'Dem'):
        return None
    pop = float(A[2])
    return (party, pop)

def makeStateResultsDict():
    for sc in stateCodes:
        read = 0;
        header = 4;
        with open(stateResultsFolder + sc + ".txt", 'r') as stateResults:
            stateResultsDict[sc] = {}
            for line in stateResults:
                if read >= header:
                    #will have to skip the first few lines
                    Area = string.split(line, "||")
                    areaInfo = string.split(Area[0],";")
                    geoidPrefix = int(areaInfo[3]) % 1000
                    if(geoidPrefix in stateResultsDict[sc].keys()):
                        d = stateResultsDict[sc][geoidPrefix]
                    else:
                        d = {"GOP":0, "Dem":0}
                    R = string.split(Area[1], '|')
                    for i in xrange(min(2, len(R))):
                        try:
                            results = getParyResFromWeirdStr(R[i])
                        except Exception as e:
                            print i, R
                            raise
                        if results == None:
                            break;
                        else:
                            d[results[0]] = d[results[0]] + results[1]
                    #maintain the current set
                    stateResultsDict[sc][geoidPrefix] = d
                read += 1;

makeStateResultsDict()
with open(simpleResultsFile, 'w') as outfile:
    pickle.dump(stateResultsDict, outfile)
