#HackGenY
#Smart Signal Lights

#Written by @AmitKochavi

import urllib,urllib2
import simplejson,json
import os.path



orig_coord = (32.080286, 34.781893)
dest_coord = (32.078884, 34.781213)

for u in range(10):

	#Google Maps

	urlMaps = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
	outMaps = simplejson.load(urllib.urlopen(urlMaps))
	#print outMaps

	#Waze

	#urlWaze = "https://www.waze.com/il-RoutingManager/routingRequest?from=x%3A" + format(orig_coord[0]) + "+y%3A" + format(orig_coord[1]) + "&to=x%3A" + format(dest_coord[0]) + "+y%3A" + format(dest_coord[1]) + "&at=0&returnJSON=true&returnGeometries=true&returnInstructions=true&timeout=60000&nPaths=3&clientVersion=4.0.0&options=AVOID_TRAILS%3At%2CALLOW_UTURNS%3At"
	urlWaze="https://www.waze.com/il-RoutingManager/routingRequest?from=x%3A34.7818933+y%3A32.0802855&to=x%3A34.779850006103516+y%3A32.08151626586914&at=0&returnJSON=true&returnGeometries=true&returnInstructions=true&timeout=60000&nPaths=3&clientVersion=4.0.0&options=AVOID_TRAILS%3At%2CALLOW_UTURNS%3At"
	outWaze = simplejson.load(urllib.urlopen(urlWaze))
	#print outWaze


	#Full trip time
	driveTime = outMaps['rows'][0]['elements'][0]['duration']['value']
	#print driveTime

	#CrossTime for segment

	segTime= outWaze['response']['results']


	segList=()
	segList2=list(segList)

	n=len(segTime)


	for k in range(n):
		
		segList2.append((segTime[k]['crossTimeWithoutRealTime'],segTime[k]['distance']))


	#print segList2

	#segList.remove(0)
	'''for b in range(n):
	 	if segList2[b][0]== 0 or segList2[b][1]==0:
	 		del segList2[b]
	 		n.Remove(str(len(segList2)))

	print segList2'''
	del segList2[0]
	del segList2[5]
	del segList2[5]
	del segList2[5]

	#print segList2
	speedList=()
	speedList2=list(speedList)
	#def calculateSpeed(infoList):
	n=len(segList2)

	def calculateSpeed(segList2):

		for i in range(n):

			g=segList2[i][1]
			h=segList2[i][0]
			segSpeed  = g/h
			speedList2.append(segSpeed)
			if segSpeed==1:
				speedList2.remove(1)
			if segSpeed==0:
				speedList2.remove(0)
			if segSpeed==2:
				speedList2.remove(2)

		print speedList2

	#Bing API Key- AsWhqrE2E4kEQqMPjoPMUg04aYNP6JM2X-hh8uo3WDWTVQHTAtEiiC6YzstjcFK9
	# latN = str(52.477213)
	# latS = str(52.356601)
	# lonW = str(-1.615194)
	# lonE = str(-1.344656)
	 
	# url = 'http://dev.virtualearth.net/REST/v1/Traffic/Incidents/'+latS+','+lonW+','+latN+','+lonE+'?key=AsWhqrE2E4kEQqMPjoPMUg04aYNP6JM2X-hh8uo3WDWTVQHTAtEiiC6YzstjcFK9'
	# response = urllib2.urlopen(url).read()
	# data = json.loads(response.decode('utf8'))
	# print data
	#resources = data['resourceSets'][0]['resources']
	#for resourceItem in resources:
		#description = resourceItem['description']
		#print description;

	calculateSpeed(segList2)

	#Google API Key- AIzaSyDlW3xoe6DKvIoe8spuw8RQRHohXTofBlc

	urlSpeed= "https://roads.googleapis.com/v1/speedLimits?path=60.170880,24.942795&key=AIzaSyDlW3xoe6DKvIoe8spuw8RQRHohXTofBlc"
	outSpeedLimit = simplejson.load(urllib.urlopen(urlSpeed))

	#print outSpeedLimit

	SpeedLimit=[8.33333,13.8889,13.8889]
	#Grading each segment/lane that is used during the drive

	#green-1-3 Clear
	#orange/yellow-4-7 Moderate
	#red-8-10 Heavy Traffic

	count=0
	gradeSegments=()
	gradeSegments2=list(gradeSegments)
	for e in range(3):
		
		count=0
		deltaSpeed=speedList2[e]-SpeedLimit[e]
		
		print deltaSpeed
		#1,2,3 points

		if deltaSpeed>0 :
			count+=1
		
		if deltaSpeed==0:
			count+=2
			

		if deltaSpeed>-2.5 and deltaSpeed<0:
			count+=3
			
		#4,5,6,7 points

		if deltaSpeed<-2.5 and deltaSpeed>-7.5:
			count=4
			
		if deltaSpeed<-7.5 and deltaSpeed>-15:
			count=5
			
		if deltaSpeed<-15 and deltaSpeed>-20:
			count=6
			
		if deltaSpeed<-25 and deltaSpeed>-30:
			count=7
			
		#8,9,10 points

		if deltaSpeed<-30 and deltaSpeed>-40:
			count=8
			
		if deltaSpeed<-40 and deltaSpeed>-60:
			count=9
			
		if deltaSpeed<=(-SpeedLimit[e]):
			count=10
			
		#Save grade for each segment in a list
		gradeSegments2.append((e,count))

	#print gradeSegments2

	finalOUTPUT=()
	finalOUTPUT1=list(finalOUTPUT)
	for p in range(3):
		finalGrade=gradeSegments2[p][1]
		finalOUTPUT1.append(finalGrade)

	#print gradeSegments
	#print finalOUTPUT1 
	finalOUTPUT2=[finalOUTPUT1[2],finalOUTPUT1[1],finalOUTPUT1[2],finalOUTPUT1[1]]
	completeName = os.path.join('/Users/AmitKochavi/Dropbox/Crossroadoptim/Code/Data', 'filename'+".txt")         
	file1 = open(completeName, "w")

	file1.write(str(finalOUTPUT1)+
				str(finalOUTPUT2))									
	file1.close()

