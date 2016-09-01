from ADSBData import ADSBData
from datetime import datetime
from traceback import format_exc
import math
import time as ttime
import sys

lastLine	= 1
time 		= datetime.now().strftime("%H")
curfile		= 'log/log_adsb_server_'+ datetime.now().strftime("%y%m%d-%H") +'.txt'
interval	= 3		##Interval to sleep
removeInterval  = 600		##Interval to remove data from main list
list_of_hex = []
list_of_invalid_hex = []
list_of_data= []

def checkHexValidity(planeHex):
	validHexList = [[16384, 17407], [24576, 28671], [32768, 197631], [204800, 208895], [212992, 218111], [221184, 225279], [229376, 233471], [253952, 258047], [262144, 266239], [270336, 274431], [278528, 282623], [286720, 290815], [294912, 295935], [303104, 304127], [311296, 315391], [327680, 331775], [344064, 348159], [360448, 364543], [368640, 369663], [376832, 380927], [385024, 386047], [393216, 394239], [401408, 405503], [409600, 413695], [425984, 430079], [434176, 435199], [442368, 446463], [450560, 454655], [458752, 462847], [475136, 476159], [483328, 484351], [491520, 495615], [499712, 500735], [507904, 511999], [524288, 528383], [540672, 544767], [557056, 561151], [565248, 569343], [573440, 577535], [589824, 593919], [606208, 607231], [614400, 615423], [622592, 623615], [630784, 634879], [638976, 643071], [647168, 648191], [655360, 692223], [696320, 697343], [700416, 701439], [704512, 708607], [712704, 716799], [720896, 724991], [729088, 733183], [737280, 741375], [745472, 749567], [753664, 757759], [761856, 765951], [770048, 771071], [778240, 782335], [786432, 790527], [794624, 798719], [802816, 806911], [811008, 815103], [819200, 823295], [827392, 828415], [835584, 836607], [851968, 917503], [1048576, 3407871], [3407872, 4456447], [4456448, 4587519], [4587520, 4718591], [4718592, 4849663], [4849664, 4980735], [4980736, 5014527], [5021696, 5025791], [5029888, 5033983], [5046272, 5047295], [5054464, 5055487], [5062656, 5063679], [5242880, 7340031], [7536640, 7667711], [7700479, 8982527], [8994816, 8999935], [9003008, 9008127], [9011200, 9016319], [9437184, 12845055], [13107200, 13144063], [13148160, 13149183], [13156352, 13157375], [13160448, 13161471], [13164544, 13165567], [13172736, 13173759], [13631488, 15208447], [15220736, 15224831], [15237120, 15241215], [15253504, 15257599], [15269888, 15273983], [15286272, 15290367], [15466496, 16777215]]
	flag = -1
	intHex = int(planeHex.upper(),16)
	if (9043968 <= intHex <= 9076735):		#Indonesia
		return True				#8A0000-8A7FFF
	elif (7667712 <= intHex <= 7700479):		#Malaysia
		return True				#750000-757FFF
	else:
		minNode = 0
		maxNode = len(validHexList)
		while(flag == -1):
			Node = (maxNode+minNode)/2
			tempvHLN0 = validHexList[Node][0]		#for efficiency
			tempvHLN1 = validHexList[Node][1]		#for efficiency
			if(intHex in range(tempvHLN0-1,tempvHLN1+1)):
				flag = 1
			elif((tempvHLN1 < intHex) and (validHexList[Node+1][0] > intHex)):
				flag = 0
			elif(intHex<validHexList[0][0]):
				flag = 0
			elif(intHex>validHexList[-1][1]):
				flag = 0
			elif(tempvHLN0 > intHex):
				maxNode=Node
			elif(tempvHLN1 < intHex):
				minNode=Node
		if (flag == 1):
			return True
		else:
			return False

def checkByArea(lat, lon, station):
	try:
		lat = float(lat)
		lon = float(lon)
	except:
		return True

	stationLat = [0,0,0,-7.279815,0,-7.291593,-7.329213,-7.366824]
	stationLon = [0,0,0,112.797507,0,112.758128,112.741370,112.775430]
	
	try:
		stationID = int(str(station)[-1])
	except:
		return True

	if (stationID == 3) or (stationID == 5) or (stationID == 6) or (stationID == 7):
		if(lat) and (lon):
			StatLocationRad = [math.radians(stationLat[stationID]),math.radians(stationLon[stationID])]
			DataLocationRad = [math.radians(lat),math.radians(lon)]
			GCD             = math.degrees(math.acos((math.sin(StatLocationRad[0])*math.sin(DataLocationRad[0]))+(math.cos(StatLocationRad[0])*math.cos(DataLocationRad[0])*math.cos(math.fabs(DataLocationRad[1]-StatLocationRad[1]))))) * 69.11511768616
			print GCD
			if GCD <= 300 :
				return True
			else:
				return False
		else:
			return True
	else:
		return False

def checkByHeading(planeHexIndex, newLat, newLon):
	if (newLat) and (newLon):
		global list_of_data
		lastDataRecord = list_of_data[planeHexIndex].dataRecord[-1][:21]
		if (lastDataRecord[5]==newLat and lastDataRecord[6]==newLon):
			return True
		elif((lastDataRecord[19]) and (lastDataRecord[20]) and (lastDataRecord[6]) and (lastDataRecord[5])):
			estTrack = (math.degrees(math.atan2(float(newLon)-float(lastDataRecord[6]),float(newLat)-float(lastDataRecord[5])))+360)%360
			return ((math.fabs(estTrack-float(lastDataRecord[19]))<=60) or (math.fabs(estTrack-float(lastDataRecord[19])-360)<=60) or (math.fabs(estTrack-float(lastDataRecord[19])+360)<=60) or (math.fabs(estTrack-float(lastDataRecord[20]))<=60) or (math.fabs(estTrack-float(lastDataRecord[20])+360)<=60) or (math.fabs(estTrack-float(lastDataRecord[20])+360)<=60) or (math.fabs(estTrack-float(lastDataRecord[20])-360)<=60))
		else :
			return True
	else :
		return True

def returnLinesAfter(fname):
	global lastLine
	linenum = lastLine-1
	data = []
	i=0
	with open(fname) as f:
		for i, l in enumerate(f):
			if (i>=linenum):
				if not len(l.strip()) == 0 :
					data.append(l)
	if (lastLine == i+1):
		return []
	else:
		lastLine = i+1
		return data

def removeDataFromMainList():
	global list_of_data
	global list_of_hex
	global removeInterval
	items_to_be_removed = []
	for f in range(0,len(list_of_data)):
        	if(math.ceil((datetime.now()-list_of_data[f].lastUpdate).total_seconds()>removeInterval)):
			items_to_be_removed.append(f)
		else:
			list_of_data[f].clearStationRecord()

	if len(items_to_be_removed) >0:
		for x in reversed(items_to_be_removed):
			list_of_data.pop(x)
			list_of_hex.pop(x)

def createJSONComplete():
        global list_of_data
        counter = 0
        b = open("dump1090/public_html/datacomplete.json","w")
	b.write("[")
        for f in range(0,len(list_of_data)):
                jsonOutput = str(list_of_data[f].returnShortDict())
		if(jsonOutput!=""):
			if(counter==0):
        	                b.write("\n{" + jsonOutput + str(list_of_data[f].returnHistory()) + "}")
        	        else :
        	                b.write(",\n{" + jsonOutput + str(list_of_data[f].returnHistory()) + "}")
                	counter+=1
	b.write("\n]")
	b.close()

def createJSON():
	global list_of_data
	counter = 0
	b = open("dump1090/public_html/data.json","w")
	b.write("[")
	for f in range(0,len(list_of_data)):
		jsonOutput = str(list_of_data[f].returnShortDict())
		if (jsonOutput!= ""):
			if math.ceil((datetime.now()-list_of_data[f].lastUpdate).total_seconds()<60) :
				if(counter==0):
					b.write("\n{" + jsonOutput + "}")
				else :
					b.write(",\n{" + jsonOutput + "}")
				counter+=1
	b.write("\n]")
	b.close()	

def createAircraftKML():
        global list_of_data
        counter = 0
        b = open("dump1090/public_html/aircraft.kml","w")
	c = open("kmlheader.txt")
	for i in c.readlines():
		b.write(i)
	c.close()
        for f in range(0,len(list_of_data)):
		KMLOutput = str(list_of_data[f].returnAircraftKML())
		if(math.ceil((datetime.now()-list_of_data[f].lastUpdate).total_seconds()<60) and KMLOutput!=""):
			b.write(KMLOutput+"\n")
	c = open("kmlfooter.txt")
        for i in c.readlines():
                b.write(i)
        c.close()
        b.close()

def createAircraftTrailKML():
        global list_of_data
        counter = 0
        b = open("dump1090/public_html/aircraft-trail.kml","w")
	c = open("kmlheader.txt")
	for i in c.readlines():
		b.write(i)
	c.close()
	c = open("kmlheaderstyle.txt")
	for i in c.readlines():
		b.write(i)
	c.close()
        for f in range(0,len(list_of_data)):
		KMLOutput = str(list_of_data[f].returnAircraftKML())
		if(math.ceil((datetime.now()-list_of_data[f].lastUpdate).total_seconds()<60) and KMLOutput!=""):
			b.write(KMLOutput+"\n")
			trailOutput = str(list_of_data[f].returnTrailKML())
			if(trailOutput!=""):
				b.write(trailOutput+"\n")
	c = open("kmlfooter.txt")
        for i in c.readlines():
                b.write(i)
        c.close()
        b.close()

def processdata(theData):
	global lastLine
	curLine = 0
	flag    = False
	dataLen = len(theData)-1
	curStation = ""	
	while(curLine<dataLen):
		if ((flag is False)or(theData[curLine][:2] == "**")) :
			while not(theData[curLine][:2] == "**"):
				curLine+=1				
			curStation=theData[curLine][2:].split()[0]
			curLine+=3
			if curLine<dataLen:
				if (theData[curLine][:2] != "**"): 
					flag = True
			else:
				 curLine+=1
		else:
			curHex = theData[curLine].split(":")[0]
			curFlightNum = theData[curLine].split(":")[2]
			curDataRecord = theData[curLine].split(":")[3:-1]+[curStation]
			if ((len(filter(None,curDataRecord))>=20) or (curDataRecord[10]!="")):
				if (curHex not in list_of_hex) and (curHex not in list_of_invalid_hex): 
					if(checkHexValidity(curHex)):
						if(curStation != ""):
							if(curFlightNum != ""):
								newADSBData=ADSBData(planeHex=curHex, dataRecord=curDataRecord, flightNumber=curFlightNum)
								#print "[1] No Station with Flight Number"
							else:
								newADSBData=ADSBData(planeHex=curHex, dataRecord=curDataRecord)
								#print "[2] No Station without Flight Number"
						else:
							if(curFlightNum != ""):
								newADSBData=ADSBData(planeHex=curHex, flightNumber=curFlightNum, dataRecord=curDataRecord, station=curStation )
								#print "[3] Station with Flight Number"
							else:
								newADSBData=ADSBData(planeHex=curHex, dataRecord=curDataRecord, station=curStation)
								#print "[4] Station without Flight Number"

						list_of_hex.append(curHex)
						list_of_data.append(newADSBData)

					else:
						list_of_invalid_hex.append(curHex)

				elif (curHex in list_of_invalid_hex):
					pass

				else:
					selectedData = list_of_data[list_of_hex.index(curHex)]
                                        try:
                                                if (len(filter(None,selectedData.dataRecord[-1]))<=len(filter(None,curDataRecord))):
                                                        print "Filter by Data content length : OK"
		                                        if (checkByHeading(list_of_hex.index(curHex),curDataRecord[5],curDataRecord[6]) and checkByArea(curDataRecord[5],curDataRecord[6],curStation)):
        		                                        if (curStation in selectedData.stationRecord):
                		                                        selectedData.stationRecord.remove(curStation)
                        		                        selectedData.stationRecord.append(curStation)
                                		                selectedData.lastUsedDataRecord = len(selectedData.dataRecord)
        		                                        if curFlightNum != "":
                		                                        selectedData.flightNumber= curFlightNum
                        		                        if(curDataRecord!=selectedData.dataRecord[-1]):
                                		                        selectedData.dataRecord.append(curDataRecord)
                                        		        else:
                                                		        print curHex + " " + curStation + " : sama"
		                                                selectedData.lastUpdate = datetime.now()
        		                        else :
      		                                        print "Filter by Data content length : Remove"
                                        except:
                                                pass
			else:
				print curHex+" removed <20 variables and no altitude"
			curLine+=1
			if (theData[curLine][:2] == "**"): 
				flag=False
counter=-1
while 1:
	try:
#	while 1:
		counter+=1
		print datetime.now()
		print lastLine
		processdata(returnLinesAfter(curfile))
		createJSON()
		createJSONComplete()
		if(counter%10 ==0):
			createAircraftKML()
			createAircraftTrailKML()
		removeDataFromMainList()
		if not (datetime.now().strftime("%H") == time):
			processdata(returnLinesAfter(curfile))
			curfile = 'log/log_adsb_server_'+ datetime.now().strftime("%y%m%d-%H") +'.txt'
			ltime = datetime.now().strftime("%H")
			lastline=1
	# when user press CTRL + C (in Linux), close socket server and exit
	except (KeyboardInterrupt, SystemExit):
		sys.exit(0)

	except:
		print '[ERR] '+format_exc().split('\n')[-2]
		pass
	ttime.sleep(0.5*interval)
