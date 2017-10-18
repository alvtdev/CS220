#!/usr/bin/python

#imports
import os
import sys
import numpy

outputFileName = "simplex.out"
#helper functions for tableau computations

#other helper functions potentially needed:
# generate tableau from constraints
def tableauGen(B, A, C):
    return

#returns sum of two tableau rows
def addRows(r1, r2):
    rsum = [0 for i in range(len(r1))]
    for i in range (len(r1)):
        rsum[i] = r1[i] + r2[i]
    return rsum

#finds position of either min or max within a row
#exclude last number from search
def findMinIndex(row):
    minNumIndex = 0
    for i in range(0, len(row)):
        print "comparing " + str(row[minNumIndex]) + " to " + str(row[i])
        if row[i] < row[minNumIndex]:
            print "new min: " + str(row[i]) + " at index " + str(i)
            minNumIndex = i
    return minNumIndex

def findPivotRow(row):
    minNumIndex = 0
    for i in range(0, len(row)):
        print "comparing " + str(row[minNumIndex]) + " to " + str(row[i])
        if (row[i] < row[minNumIndex] and row[i] > 0) or (row[minNumIndex] < 0):
            print "new min: " + str(row[i]) + " at index " + str(i)
            minNumIndex = i
    return minNumIndex
#finding max index may not be necessary for maximization
# but will be left here in case.
def findMaxIndex(row):
    maxNumIndex = 0
    for i in range(0, len(row)-1):
        if row[i] > row[maxNumIndex]:
            maxNumIndex = i
    return maxNumIndex

#multiplies a row by a constant 
def multRow(row, const):
    newRow = []
    for i in range(0, len(row)):
        newRow.append(const*row[i])
    return newRow

#checks solution for optimality
# if optimal return "OPTIMAL", else return "SUBOPTIMAL"
# takes in a row as input, should only be used on last row of tableau
def checkSol(row):
    #if all entries are non-negative, return optimal
    isOptSol = "OPTIMAL"
    for i in row:
        #if a negative entry is found, return suboptimal
        if i < 0:
            isOptSol = "SUBOPTIMAL"
    return isOptSol

#takes matrix of ratios as input and checks for unbounded
#if unbounded, write "+inf" to output file and exits
#NOTE: fix - checking for unbounded is not simply finding "+inf"
#  dividing by zero throws an error
#  possible solution: take in array of pivot values and check if any are zero
#    -must create pivot array first. 
def checkUnbounded(row): 
    for i in row:
        if i == 0.0:
            file = open(outputFileName, 'w')
            file.write("+inf") 
            file.close() 
            exit(0)
    return

#takes B as input, checks for negative val (negative = bounded infeasible)
#TODO: fix - only x>=0 is implicit, not s>=0
def checkInfeasible(row):
    for i in row:
        if i < 0:
            file = open(outputFileName, 'w') 
            file.write("bounded-infeasible")
            file.close()
            exit(0)
    return

#takes in tableau as input, print ctx & elements of x to file
def printOptSol(tableau):
    file = open(outputFileName, 'w') 
    #first write ctx
    file.write(str(tableau[-1][-1]))
    #TODO: then append x values
    file.close()
    exit(0)
    return
        

#test checkUnbounded, checkInfeasible, printOptSol
#testrow = [5, 10, float("+inf")]
#checkUnbounded(testrow)
#testRow = [5, -3, 7, 9]
#checkInfeasible(testRow)
testTableaux = [[0, 1, 0, 0, 0, 12], [0, 0, 1, 0, 0, 14], 
            [1, 0, 0, 0, 0, 15], [0, 0, 0, 0, 0, 132]]
#printOptSol(testTableau)

#get arguments, print usage if incorrect
if (len(sys.argv) > 2):
    print "usage: python assn1.py <filename>"

#set filename, get contents of file and put into list
filename = sys.argv[1]

#if filename doesn't exist in the current directory, output error and exit
if (not(os.path.exists(filename))):
    print "Error: " + filename + " not found"
    exit(0)

#otherwise, continue with simplex program
with open(filename, 'rb') as file:
    inputLines = [row.strip().split() for row in file]

#convert strings in array to floats
inputLines = [[float(x) for x in lst] for lst in inputLines]

#TODO:separate input matrix to A, b, c^t
#     generate simplex tableau

#separate input into vars & matrices
numConstraints = inputLines[0][0]
numVars = inputLines[0][1]

B = inputLines[1]
C = inputLines[2]
A = inputLines[3:]

#test output to check input separation validity
"""
print "numConstraints = " + str(numConstraints)
print "numVars = " + str(numVars)
print "B = " + str(B)
print "C = " + str(C)
print "A = " + str(A) 
"""

#TODO: generate tableau
#tableau = []
tableau = [[-1.0, 1.0, 1.0, 0.0, 0.0, 11.0], [1.0, 1.0, 0.0, 1.0, 0.0, 27.0],
            [2.0, 5.0, 0.0, 0.0, 1.0, 90.0], [-4.0, -6.0, 0.0, 0.0, 0.0, 0.0]]

#var to track if solution is optimal
optSolStat = "SUBOPTIMAL" 
#initial check to see if solution is optimal 
#  (for cases where the first solution is actually optimal)
optSolStat = checkSol(tableau[-1])
#list that stores solved rows
#apply simplex algorithm
while optSolStat == "SUBOPTIMAL":
    #find pivot index
    print "Finding pivot column"
    pivotCol = findMinIndex(tableau[-1])
    print pivotCol
    
    #create row of pivot values for unbounded check
    pivotVals = []
    for list in tableau:
        #for j in solvedRows:
        #    if i != j:
        pivotVals.append(list[pivotCol])
    print pivotVals

    #check pivot vals for 0 (unbounded solution)
    checkUnbounded(pivotVals)

    #calculate ratios
    print "Calculating Ratios"
    ratios = []
    for i in range(0, len(tableau)-1):
        if (pivotVals[i] ==0):
            ratios.append(float("+inf"))
        else:
            ratios.append(tableau[i][-1]/pivotVals[i])
    print ratios

    #determine min ratio
    print "Finding pivot row" 
    pivotRow = findPivotRow(ratios)
    print pivotRow

    #TODO:perform pivot
    #   FIXME: ignore values in last column with non-negative elements in corresponding column
    #first check coefficient of element at [pivotRow][pivotColumn]
    #  if coefficient is not 1, divide entire row by 1/coeff
    if tableau[pivotRow][pivotCol] != 1.0:
        tableau[pivotRow] = multRow(tableau[pivotRow], 1.0/tableau[pivotRow][pivotCol]) 
        pivotVals[pivotRow] = 1
        print "NEW MATRIX" 
        for list in tableau:
            print list

    for i in range(0, len(tableau)):
        #only perform following operations on rows that are not the pivot row
        if i != pivotRow:
            #determine constant
            multConst =-(pivotVals[i]/pivotVals[pivotRow])

            # multiply pivot row by constant
            tempRow = multRow(tableau[pivotRow], multConst)

            #sum rows, assign new value to proper list position
            tableau[i] = addRows(tableau[i], tempRow)

    print "CURRENT TABLEAU"
    for list in tableau:
        print list

    print "\n"
    #check if new solution is optimal
    optSolStat = checkSol(tableau[-1])

#now that solution is bounded-feasible and optimal, output to file
if optSolStat == "OPTIMAL":
        #print ctx and each element of x
    print "OPTIMAL SOLUTION FOUND" 
    printOptSol(tableau)

#NOTE: check for unbounded and bounded infeasible when determining ratios
#       e.g. if b/0 (inf) => unbounded
#           output "+inf" to file then exit(0)
#       e.g. if any ratio is negative => bounded-infeasible
#           output "bounded-infeasible" to file then exit(0)


#note: Bland's Rule
# 1. select lowest-numbered nonbasic column with negative cost
# 2. choose the one with the lowest ratio between RH + coefficient in pivot
#    if min ratio is shared by more than 1 row, 
#    choose row with lowest numbered column
