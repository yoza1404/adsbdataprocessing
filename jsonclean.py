listtanggal = [] 
for var1 in range(14,26):
	for var2 in range (0,24):
		listtanggal.append("1506"+str(var1)+"-"+str(var2).zfill(2)) 
listtanggal= listtanggal[17:]

import urllib2
import json
import csv

for tanggalan in listtanggal:
	print tanggalan
	u = open("dump1090/public_html/newjson/"+tanggalan+".json").readlines()
	newstring = []
	for y in u :
		newstring.append(y.decode('string_escape'))
	resultFile = open("json/"+str(tanggalan)+".json",'wb')
	for y in newstring :
		resultFile.write(y)
	resultFile.close()
