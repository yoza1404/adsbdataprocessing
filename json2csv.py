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
#	u = urllib2.urlopen('http://116.68.248.195/~yoza/TA/new-client-server/aktual/dump1090/public_html/newjson/150615-00.json')
	u = open("json/"+tanggalan+".json")
	x = json.load(u, strict=False)
	u.close()

	listkosong = [["AA", "CAT", "CS", "FS", "CA", "DR", "UM", "ID", "LAT", "LON", "NIC", "NUCR/ NACV", "FL", "AC", "M", "Q", "GNSS", "HAE", "VSRC", "VR", "VRF", "HAB", "TT", "HDG", "AST", "IAS", "TAS", "GS", "MACH", "MCP", "RA", "TR", "FMS", "QNH", "FCU", "PA", "PS", "ACAS", "ALRT", "SPI", "GR", "IC", "SSC", "IFR", "TS", "RI", "CC", "SL", "ADSB", "BDS40", "BDS50", "BDS60", "BDS65", "FMT30", "BDS61", "WDIR", "WSPD", "TEMP", "AGE_0", "AGE_4", "AGE_5", "AGE_11", "AGE_16", "AGE_17_0e", "AGE_17_0o", "AGE_17_1", "AGE_17_5e", "AGE_17_5o", "AGE_17_19", "AGE_17_28", "AGE_17_30", "AGE_17_31", "AGE_20_20", "AGE_20_40", "AGE_20_50", "AGE_20_60", "AGE_21_20", "AGE_21_40", "AGE_21_50", "AGE_21_60", "TIMESTAMP", "TIMEOUT", "STATION ID"
	]]
	for z in range(0,len(x)):
	    for z1 in range(0,len(x[z]['history'])):
	        listkosong.append([x[z]['hex'],"",x[z]['flight']]+x[z]['history'][z1])

	resultFile = open("csv/"+str(tanggalan)+".csv",'wb')
	wr = csv.writer(resultFile, dialect='excel')
	wr.writerows(listkosong)
	resultFile.close()
