import string
import pickle

stateResultsFolder= "StateResults/"
simpleResultsFile = "simpleResults.pickle"
csvResultsFile2012 = "US_elect_county.csv"
simpleResultsFile2012 = "simpleResults2012.pickle"
stateResultsDict2012 = {}

stateCodes = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
stateResultsDict = {}

# From politico data

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
    #make percents
    for state in stateResultsDict.keys():
        for county in stateResultsDict[state].keys():
            d = stateResultsDict[state][county]
            total = d["GOP"] + d["Dem"]
            if(total == 0):
                percent = 0.5
            else:
                percent = round(float(d["Dem"]) / total, 3)
            stateResultsDict[state][county] = percent


makeStateResultsDict()
with open(simpleResultsFile, 'w') as outfile:
    pickle.dump(stateResultsDict, outfile)

#from 2012 results
def makeStateResults2012Dict():
    for sc in stateCodes:
        read = 0;
        header = 1;
        with open(csvResultsFile2012, 'r') as stateResults:
            for line in stateResults:
                if read >= header:
                    vals = string.split(line, ',')
                    state = vals[0]
                    if state not in stateResultsDict2012.keys():
                        stateResultsDict2012[state] = {}
                    fipsPrefix = int(vals[2]) % 1000
                    try:
                        percent = 1 - round(float(vals[4]) / 100.0, 3)
                    except:
                        percent = 0
                    stateResultsDict2012[state][fipsPrefix] = percent
                read += 1

makeStateResults2012Dict()

with open(simpleResultsFile2012, 'w') as outfile:
    pickle.dump(stateResultsDict2012, outfile)



