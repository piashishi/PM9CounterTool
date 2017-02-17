from __future__ import division

import re
import os
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

#filter counter which value is zero
filterZero = True

def getStartAndEndTime(fileName):
	#fileName: A20161222.1030+0800-20161222.1045+0800_SHSAEGW10BNK_73.xm
	timeRe = re.compile('\d+\.\d+')
	tmp = timeRe.findall(fileName)
	startTime = datetime.strptime(tmp[0], '%Y%m%d.%H%M')
	endTime = datetime.strptime(tmp[1], '%Y%m%d.%H%M')
	return startTime, endTime


# xml template
# ...
# <PMMOResult>
# ...
# </PMMOResult>
# <PMMOResult>
# 	<MO>
# 		<DN>FING-SHSAEGW10BNK/FPNODE-AS13-0/PCCR-AbnormalSig_icmp</DN>
# 	</MO>
# 	<PMTarget measurementType="PCCrule_statistics" version="140">
# 		<m3076c0001>8331945</m3076c0001>
# 		<m3076c0002>2411689</m3076c0002>
# 	</PMTarget>
# </PMMOResult>
def getCounterValue(filename, startTime, counter, counterHash={}):
	counterInFile = -1
	for event, elem in ET.iterparse(filename):
		if event == 'end':
			if counterInFile != 1:
				if elem.tag == 'PMMOResult':
					if counterInFile == -1: #first time
						counterInFile = 0
					elif counterInFile == 0:  #file haven't counter
						return 

			if elem.tag == 'DN':
				#remove NG name
				name = "/".join(elem.text.split('/')[1:])
			if elem.tag == counter:
				counterInFile = 1
				if int(elem.text) == 0 and filterZero:
					continue
				if name not in counterHash.keys():
					counterHash[name] = []
					counterHash[name].append((startTime, int(elem.text)))
				else:
					counterHash[name].append((startTime, int(elem.text)))
		elem.clear() # discard the element


def parseCounter(counterDir="", startTime="", endTime="", counter=""):
	counterHash = {}
	st = datetime.strptime(startTime, '%Y%m%d%H%M') 
	et = datetime.strptime(endTime, '%Y%m%d%H%M')
	for root, dirs, files in os.walk(counterDir, topdown=False):
		for name in files:
			if name.endswith("xml"):
				#find file match the rule
				start, end = getStartAndEndTime(name)
				if start >= st and end <= et:
					getCounterValue(os.path.join(root, name), start, counter, counterHash)
	return counterHash


def draw(key, counterHash={}):
	time = [ x[0] for x in counterHash[key] ]
	value = [ x[1] for x in counterHash[key] ]
	data = [go.Scatter(
	            x= time,
	            y= value
	    )]
	py.plot(data, filename='counter-image')
 
# py.plot(data, filename='counter-image')
