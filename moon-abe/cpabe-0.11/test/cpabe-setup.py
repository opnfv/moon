#!/usr/bin/python
import os.path
import sys
from subprocess import call

c_prog = "cpabe-setup"
c_file = "/usr/local/bin/" + c_prog

if(os.path.isfile(c_file)):
	call([c_prog])

elif(os.path.isfile("./" + c_prog)):
	print "Warning: missing file %s using binary in local repository" % c_file
	call(["./" + c_prog])

else:
	sys.exit(c_prog + " was not found. Be sure that the C library cpabe is installed before running this program")
