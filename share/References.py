#!/bin/python
import os
import sys
import configparse

cache_dir=configparse.cfg["cache_dir"]
script = str(os.path.dirname(os.path.realpath(sys.argv[0])))
os.chdir(script)

out = cache_dir+"/output.bib"
inp = cache_dir+"/dois.txt"
f= open(out,'w+')
fp = open(inp, 'r')
for line in fp:
	doi = line.split(' ')[0]
	cmd = os.popen('doi2bib ' + doi).read()
	f.write(cmd)
print ("\\nocite{"+"*}")
print ("\\printbibliography[heading=none]")
