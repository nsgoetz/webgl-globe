import json
import string
import pickle

csvFileName = "Gaz_tracts_national.txt"
jsonFileName = "US_gaz_population.json"
stateResultsFolder= "StateResults/"
simpleResultsFileName = "../simpleResults.pickle"
simpleResults2012FileName = "../simpleResults2012.pickle"

seperator = '\t'


data2012 = []
data2016 = []
maximum = 0
testNum = 64000
resolution = 4.5  # sqrt of max number of lines number of lines per 1x1 lat long box

stateCodes = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

pickle_data=open(simpleResultsFileName).read()
stateResultsDict2016 = pickle.loads(pickle_data)
pickle_data2=open(simpleResults2012FileName).read()
stateResultsDict2012 = pickle.loads(pickle_data2)

#note have to treat AK special - it doesn't report by county
def getColorForGeo(state, geoid, resultsDict):
    # -1 for no result, otherwise the percentage dem from 0 to 1
    if state not in resultsDict.keys():
        return -1
    if state == "AK":
        geoid = 0
    geoidlen = 11
    county = (geoid / 10**(geoidlen - (2 + 3))) % 1000
    if (county not in resultsDict[state].keys()):
        print county, state
        return -1
    percent = float(resultsDict[state][county])
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
                dataDict[(lat, long)] = (old[0] + pop, old[1], old[2])
            else:
                color2016 = getColorForGeo(lineArray[0], int(lineArray[1]), stateResultsDict2016)
                color2012 = getColorForGeo(lineArray[0], int(lineArray[1]), stateResultsDict2012)
                dataDict[(lat, long)] = (pop, color2012, color2016)
            maximum = max(dataDict[(lat, long)][0], maximum)
        read += 1

for key in dataDict.keys():
    lat = key[0]
    long = key[1]
    pop = dataDict[key][0]
    color2012 = dataDict[key][1]
    color2016 = dataDict[key][2]
    data2012.append([lat, long, float(pop)/float(maximum), color2012])
    data2016.append([lat, long, float(pop)/float(maximum), color2016])

#data = map(lambda A: [A[0], A[1], float(A[2])/float(maximum)], data)
#flatten
data2012 = [i for sublist in data2012 for i in sublist]
data2016 = [i for sublist in data2016 for i in sublist]

with open(jsonFileName, 'w') as outfile:
    writeData = [["2016", data2016], ["2012", data2012]]
    json.dump(writeData, outfile, indent=None, sort_keys=True, separators=(',',':'))