import json
import string
import pickle

csvFileName = "Gaz_tracts_national.txt"
jsonFileName = "US_gaz_population.json"
stateResultsFolder= "StateResults/"
simpleResultsFileName = "../simpleResults.pickle"

seperator = '\t'


data = []
maximum = 0
testNum = 64000
resolution = 4.5  # sqrt of max number of lines number of lines per 1x1 lat long box

stateCodes = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

pickle_data=open(simpleResultsFileName).read()
stateResultsDict = pickle.loads(pickle_data)

#note have to treat AK special - it doesn't report by county
def getColorForGeo(state, geoid):
    # -1 for no result, otherwise the percentage dem from 0 to 1
    if state not in stateResultsDict.keys():
        return -1
    geoidlen = 11
    county = (geoid / 10**(geoidlen - (2 + 3))) % 1000
    if (county not in stateResultsDict[state].keys()):
        print county, state
        return -1
    results = stateResultsDict[state][county]
    total = results["GOP"] + results["Dem"]
    if(total == 0):
        percent = 0.5
    else:
        percent = round(float(results["Dem"]) / total, 3)
    return percent

dataDict = {}
color = 0x0000FF #blue
with open(csvFileName, 'r') as csv:
    read = -1;
    for line in csv:
        if read > 0:
            lineArray = string.split(line, seperator)
            assert(len(lineArray) == 10)
            pop = int(lineArray[2])
            lat = round(round(float(lineArray[8]) * resolution, 0) / resolution, 2)
            long = round(round(float(lineArray[9]) * resolution, 0) / resolution, 2)
            if (lat, long) in dataDict.keys():
                old = dataDict[(lat, long)]
                dataDict[(lat, long)] = (old[0] + pop, old[1])
            else:
                dataDict[(lat, long)] = (pop, getColorForGeo(lineArray[0], int(lineArray[1])))
            maximum = max(dataDict[(lat, long)][0], maximum)
        read += 1

for key in dataDict.keys():
    lat = key[0]
    long = key[1]
    pop = dataDict[key][0]
    color = dataDict[key][1]
    data.append([lat, long, float(pop)/float(maximum), color])

#data = map(lambda A: [A[0], A[1], float(A[2])/float(maximum)], data)
#flatten
data = [i for sublist in data for i in sublist]

with open(jsonFileName, 'w') as outfile:
    writeData = [["2000", data]]
    json.dump(writeData, outfile, indent=None, sort_keys=True, separators=(',',':'))