#!/usr/bin/python

import re
import sys

def changeThings():

	#open File 
	file = open("TCDB.faa",'rw+')

	#Read Contents of File into a list
	#which is seperated using the newlines
	contents = file.read().split('\n')

	#line number pointer for the list
	line = 0

	#Prepare Sequence ID, Accession, and Sequence variables
	seqId = ''
	seqAcc= ''
	sequence = ''

	#print(len(contents))

	#Match parameters for regular expression for sequence

	search = r'>[A-Za-z]+\|TC-DB\|(.*?)\|([\w\.]+)'

	
	while line < len(contents)-1:

		if contents[line][0][0] == '>':

		
			seqInfo = re.match(search,contents[line],re.M|re.I)

			if seqInfo:
				seqId = seqInfo.group(2)
				seqAcc = seqInfo.group(1)
				line += 1

			try:

				while contents[line][0][0] != ">":

						
					sequence+=contents[line].replace('\n','')
					line += 1
			
			except IndexError:
				pass

			print('%s-%s\t%s' % (seqId,seqAcc,sequence))


		
			sequence = ''



if __name__ == "__main__":

	changeThings()
