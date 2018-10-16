#!/usr/bin/env python

import os, sys
i=0
statusInfo=[]
pathInfo=os.listdir(path='.')
#print(pathInfo)

while i<len(pathInfo):
	statusInfo.append(os.stat(pathInfo[i]).st_mtime)
	i=i+1
#print(statusInfo)

n=len(statusInfo)
for i in range(n):
	for j in range(n-i-1):
		if statusInfo[j]>statusInfo[j+1]:
			statusInfo[j],statusInfo[j+1]=statusInfo[j+1],statusInfo[j]	
			pathInfo[j],pathInfo[j+1]=pathInfo[j+1],pathInfo[j]

#print(pathInfo)
#print(statusInfo)

i=1
while i<=(sys.argv[1]):
	print(pathInfo[-i])
	i=i+1