#!/usr/bin/python

#imports
import sys
import numpy

#get arguments, print usage if incorrect
if (len(sys.argv) > 2):
    print "usage: python assn1.py <filename>"
else:
    print 'Opening '+ str(sys.argv[1])

#set filename, get contents of file and put into list
filename = sys.argv[1]
with open(filename, 'rb') as file:
    inputLines = [row.strip().split() for row in file]
#print inputLines

#convert strings in array to floats
inputLines = [[float(x) for x in lst] for lst in inputLines]
#print inputLines

#TODO:separate input matrix to A, b, c^t
#     generate simplex tableau
