import urllib
import string

stateCodes = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

def URLForState(stateCode):
    s = "https://s3.amazonaws.com/origin-east-elections.politico.com/mapdata/2016/%s_20161108.xml?cachebuster=20161109202100" % stateCode
    return s

opener = urllib.URLopener()
failed = 0

subfolder = "StateResults"

fileList = [URLForState(sc) for sc in stateCodes]

for sc in stateCodes:
  print "downloading %s ... " % sc,
  try:
    opener.retrieve(URLForState(sc), subfolder + "/" + sc + ".txt")
    print " done \n"
  except:
    failed += 1
    print " FAILED\n"
    print "\n COULD NOT RETRIEVE: " + sc + " \n\n"

print "\nALL done: %d fails\n" % failed
