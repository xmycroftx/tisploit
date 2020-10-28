# tisploit
tisploit is a collection of timing attack exploits.  They are, by their very nature, fickle and subject to many environmental conditions.

## basicauth.py

this script, attempts to use the timing variation in real users and nonuser inputs to an http basic auth interface.

The premise is, find an oracle (in this case we use a random string) and use the Aggregate response time as the baseline.  We made sure garbage (random string) didn't existas a user for the purposes of this test but the random oracle has proven effective in practical attacks.

### usage: ./basicauth.py hostname username attempts

TODO:
The fudge factor (x < meant + 1.97 * sdt) should really be a kalman filter.
