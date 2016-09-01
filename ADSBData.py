from datetime import datetime, timedelta
import math
import os

class ADSBData:
	def __init__(self, planeHex, flightNumber="", dataRecord=[], station="INIT" ):
		self.planeHex 		= planeHex.upper()
		self.flightNumber	= flightNumber.upper()
		self.dataRecord 	= []
		self.stationRecord	= []
		self.lastUpdate 	= datetime.now()
		self.lastUsedDataRecord = -1
		self.stationRecord.append(station)
		self.dataRecord.append(dataRecord)

	def clearStationRecord(self):
		while (len(self.stationRecord)>1):
			self.stationRecord.pop(0)
		pass

	def returnHistory(self):
		if len(self.dataRecord)>1 :
			return ', "history" :' + str(self.dataRecord).replace("'",'"')
		else:
			return ""
	
	def returnShortDict(self):
		if len(self.dataRecord)>1 :
			curValidPos = 1
			
			if(self.dataRecord[-1][4] != ""):
				curSquawk = self.dataRecord[-1][4]
			else:
				curSquawk = "----"

			if(str(self.flightNumber) != ""):
				curFlightNum=self.flightNumber
			else:
				curFlightNum = 'N/A'
			
			if(self.dataRecord[-1][5] != ""):
				curLat = self.dataRecord[-1][5]
			else:
				curLat = 0.0
				curValidPos = 0
				
			if(self.dataRecord[-1][6] != ""):
				curLon = self.dataRecord[-1][6]
			else:
				curLon = 0.0
				curValidPos = 0

			if(self.dataRecord[-1][10] != ""):
				curAlt = self.dataRecord[-1][10]
			else:
				curAlt = '"N/A"'

			if(self.dataRecord[-1][16] != ""):
				curVRate = self.dataRecord[-1][16]
			else:
				curVRate = '"N/A"'
			
			if(self.dataRecord[-1][19] != ""):
				curTrack = self.dataRecord[-1][19]
			else:
				curTrack = '"N/A"'

			if(self.dataRecord[-1][24] != ""):
				curSpeed = self.dataRecord[-1][24]
			else:
				curSpeed = '"N/A"'

			return '"hex": "'+str(self.planeHex)+'", "squawk": "'+ str(curSquawk) + '", "flight": "'+ str(curFlightNum) +'", "lat": '+ str(curLat) + ', "lon": '+ str(curLon) +', "validposition": '+ str(curValidPos) +', "altitude": '+ str(curAlt) +', "vert_rate": '+ str(curVRate) +', "track": '+ str(curTrack) +', "validtrack": 1, "speed": '+ str(curSpeed) +', "messages": '+str(len(self.dataRecord))+', "seen": '+str(math.ceil((datetime.now()-self.lastUpdate).total_seconds()))+', "station": "'+str(self.stationRecord[-1])+'"'
		else:
			return ""
			
		
	def returnAircraftKML(self):
		if len(self.dataRecord)>1 :
			curValidPos=1
			if(str(self.flightNumber) != ""):
				curFlightNum=self.flightNumber
			else:
				curFlightNum = 'N/A'
			
			if(self.dataRecord[-1][5] != ""):
				curLat = self.dataRecord[-1][5]
			else:
				curLat = 0.0
				curValidPos = 0
				
			if(self.dataRecord[-1][6] != ""):
				curLon = self.dataRecord[-1][6]
			else:
				curLon = 0.0
				curValidPos = 0

			curReg = ""				##need more insights about this
			curType = ""				##need more insights about this
			
			if(self.dataRecord[-1][10] != ""):
				curAlt = self.dataRecord[-1][10]
			else:
				curAlt = '"N/A"'
				curValidPos = 0

			if(self.dataRecord[-1][9] != ""):
				curFLevel = self.dataRecord[-1][9]
			else:
				curFLevel = '"N/A"'
			
			if(self.dataRecord[-1][19] != ""):
				curTrack = self.dataRecord[-1][19]
			else:
				curTrack = '"N/A"'
				curValidPos = 0

			if (curValidPos ==1):
				return "<Placemark><description>Flight : " + str(curFlightNum) + "\nReg : " + str(curReg) + "\nHex : " + str(self.planeHex) + "\nType : " + str(curType) + "\nFlt Level : " + str(curFLevel) + "</description><name>" + curFlightNum + " " + str(curReg) + " " + self.planeHex + " " + str(curType) + " " + str(curFLevel) + "</name><styleUrl>#mystyle" + str(int(float(curTrack)/5)).zfill(2) + "</styleUrl><visibility>1</visibility><Point><altitudeMode>absolute</altitudeMode><coordinates>" + str(curLon) + "," + str(curLat) + "," + str(int(float(curAlt)*0.3048)) + "</coordinates></Point></Placemark>"
			else:
				return ""
		
	def returnTrailKML(self): 
		if len(self.dataRecord)>1 :
			listOfCoordinate = []
			if(str(self.flightNumber) != ""):
				curFlightNum=self.flightNumber
			else:
				curFlightNum =self.planeHex
			
			for x in self.dataRecord:
				if((x[6] != "") and (x[5] != "") and (x[10] != "")):
					coordInfo = str(x[6]+","+x[5]+","+str(int(float(x[10])*0.3048)))
					if (coordInfo not in listOfCoordinate):
						listOfCoordinate.append(coordInfo)

			if len(listOfCoordinate)>1:
				strReturn = "<Placemark> <name>" + curFlightNum + "-trail</name> <styleUrl>#mystyle72</styleUrl> <visibility>1</visibility> <LineString> <extrude>0</extrude> <tessellate>1</tessellate> <altitudeMode>absolute</altitudeMode> <coordinates> "
				for i in listOfCoordinate:
					strReturn+=i+" "
				strReturn+= "</coordinates> </LineString> </Placemark>"
				return strReturn
			else:
				return ""
