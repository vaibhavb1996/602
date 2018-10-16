#Copyright 2018 Vaibhav Bansal vbansal@bu.edu

import sys
i=1
while (i<len(sys.argv)):
	if i<5:
		sys.stdout.write(sys.argv[i]+"\n")
		
	else:
		sys.stderr.write(sys.argv[i]+"\n")
		
	i=i+1
