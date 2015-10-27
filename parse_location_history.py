import sys, os, json, datetime, time, xml.dom.minidom
from decimal import *
from optparse import OptionParser
parser = OptionParser(usage='usage: %prog [-f | --file] inputJSON [-s | --start] month/day/year [-e | --end] month/day/year [-o | --output] outputKML')
parser.add_option("-s", "--start", action="store", type="string", dest="startDate")
parser.add_option("-e", "--end", action="store", type="string", dest="endDate")
parser.add_option("-f", "--file", action="store", type="string", dest="file")
parser.add_option("-o", "--output", action="store", type="string", dest="output")

(options, args) = parser.parse_args()
if not options.output:   # if filename is not given
	parser.error('Output file not given')
if not options.startDate:
	parser.error('Start date not given')
if not options.endDate:
	options.endDate = options.startDate
if not options.file:
	parser.error('Input JSON not given')

getcontext().prec = 7
dates = []

#from here: http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def createKML(locations):
	# This constructs the KML document from the CSV file.
	kmlDoc = xml.dom.minidom.Document()

	kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
	kmlElement.setAttribute('xmlns', 'http://earth.google.com/kml/2.2')
	kmlElement = kmlDoc.appendChild(kmlElement)
	documentElement = kmlDoc.createElement('Document')
	
	
	

	startDate = map (int, options.startDate.split("/"))
	endDate = map (int, options.endDate.split("/"))
	startDateTime = datetime.date(startDate[2],startDate[0],startDate[1])
	# minTime = time.mktime(startDateTime.timetuple()) * 1000
	endDateTime = datetime.date(endDate[2],endDate[0],endDate[1]+1)
	# maxTime = time.mktime(endDateTime.timetuple()) * 1000

	for singledate in daterange(startDateTime, endDateTime):
		dates.append(singledate)
	for i in range(0,len(dates)):
		if i < len(dates)-1:
			print dates[i]
			print dates[i+1]
			minTime = time.mktime(dates[i].timetuple()) * 1000
			maxTime = time.mktime(dates[i+1].timetuple()) * 1000
			placemarkElement = kmlDoc.createElement('Placemark')
			trackElement = kmlDoc.createElement('gx:Track')
			placemarkElement.appendChild(trackElement)
			for point in locations:
				timestampMs = int(point["timestampMs"])
				if  minTime < timestampMs < maxTime:
					# if "activitys" in point:
						# if point["activitys"][0]["activities"][0]["type"] == "onFoot":
							
							whereElement = kmlDoc.createElement('gx:coord')
				  			whenElement = kmlDoc.createElement('when')
							whereText = kmlDoc.createTextNode(str(Decimal(point["longitudeE7"]) / Decimal(10000000)) + " " + str(Decimal(point["latitudeE7"]) / Decimal(10000000)) + " 0")
							whenText = kmlDoc.createTextNode(str(timestampMs))
							whereElement.appendChild(whereText)
							whenElement.appendChild(whenText)
							trackElement.appendChild(whereElement)
							trackElement.appendChild(whenElement)
			documentElement.appendChild(placemarkElement)
	documentElement = kmlElement.appendChild(documentElement)
	kmlFile = open(options.output, 'w')
	kmlFile.write(kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))


with open(options.file, 'rb') as f:
	data = json.load(f)
	createKML(data["locations"])
	

