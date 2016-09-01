listtanggal = [] 
for var1 in range(14,26):
	for var2 in range (0,24):
		listtanggal.append("1506"+str(var1)+"-"+str(var2).zfill(2)) 
listtanggal= listtanggal[17:]

import urllib2
import json
import csv

for tanggalan in listtanggal:
	u = open("json/"+tanggalan+".json")
	x = json.load(u, strict=False)
	u.close()

	for z in range(0,len(x)):
		print x[z]['hex']
