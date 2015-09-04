#!/usr/bin/python
import os, sys
from subprocess import call

c_prog = "cpabe-attrList"
c_file = "/usr/local/bin/" + c_prog

if(os.path.isfile(c_file)):
	args = [c_prog] + sys.argv[1::]
	call(args)

elif(os.path.isfile("./" + c_prog)):
	print "Warning: missing file %s using binary in local repository" % c_file
	args = ["./" + c_prog] + sys.argv[1::]
	call(args)

else:
	sys.exit(c_prog + " was not found. Be sure that the C library cpabe is installed before running this program")
