#!/usr/bin/python

#imports
import sys
import numpy

#helper functions for tableau computations

#other helper functions potentially needed:
# generate tableau from constraints
# select pivot 

#returns sum of two tableau rows
def addRows(r1, r2):
    rsum = [0 for i in range(len(row1))]
    for i in range (len(row1)):
        rsum[i] = r1[i] + r2[i]
    return rsum

#finds position of either min or max within a row
#exclude last number from search
def findMaxIndex(row):
    maxNumIndex = 0
    for i in range(0, len(row)-1):
        if row[i] > row[maxNumIndex]:
            maxNumIndex = i
    return maxNumIndex

def findMinIndex(row):
    minNumIndex = 0
    for i in range(0, len(row)-1):
        if row[i] < row[minNumIndex]:
            minNumIndex = i
    return minNumIndex

#multiplies a row by a constant 
def multRow(row, const):
    newRow = []
    for i in range(0, len(row)):
        newRow.append(const*row[i])
    return newRow

#checks solution for optimality
# if optimal return "OPTIMAL", else return "SUBOPTIMAL"
# takes in a row as input, should only be used on last row of tableau
# TODO: expand this or create new helper functions to determine 
#        bounded-infeasible & unbounded
def checkSol(row):
    #if all entries are non-negative, return optimal
    isOptSol = "OPTIMAL"
    for i in row:
    #if a negative entry is found, return suboptimal
        if i < 0:
            isOptSol = "SUBOPTIMAL"
    return isOptSol


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
