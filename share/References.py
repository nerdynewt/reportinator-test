#!/bin/python
import os
import sys
script = str(os.path.dirname(os.path.realpath(sys.argv[0])))
os.chdir(script)

out = "../_assets/output.bib"
inp = "../_assets/dois.txt"
f= open(out,'w+')
fp = open(inp, 'r')
for line in fp:
	doi = line.split(' ')[0]
	cmd = os.popen('doi2bib ' + doi).read()
	f.write(cmd)
print ("\\nocite{"+"*}")
print ("\\printbibliography[heading=none]")