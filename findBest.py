#!/usr/bin/env python

import bz2
from collections import defaultdict

def readFile():

	#open the file
	file = bz2.BZ2File('RS.txt.bz2')


	#read the lines
	contents = file.readlines()

	#print(len(contents))i

	proteins = defaultdict(list)

	#Loop throught list creating a dictionary
	for line in contents:	

		info = line.split('\t')

		ID = info[0]
		ID2 = (info[1],info[3].replace('\n',''));

		#add to dictionary	
		proteins[ID].append(ID2)

		i+=1

		#if ID2 in proteins[ID]:

			#print('%d\t%s\t%s\t%s' % (len(proteins[ID]),ID,ID2[0],ID2[1])) 
		

	return proteins

def findBest(proteins):

	ID1=''
	ID2=''
	prob=''
	seqLen=0
	for key in proteins:

		best = sorted(proteins[key],key=lambda x: x[1], reverse=True)[0]

		#print('%d\t%s\t%s\t%s' % (len(proteins[key]),key,best[0],best[1]))
	
		#print(len(proteins[key]))

		if len(proteins[key]) > seqLen:

			prob = best[1]

			ID1 = key
			ID2 = best[0]

			seqLen = len(proteins[key]) 


	
	print('%s\t%s\t%s\t%d' % (ID1,ID2,prob,seqLen))

if __name__ == "__main__":

	proteins = readFile()

	findBest(proteins)
