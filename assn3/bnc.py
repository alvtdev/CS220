#!/usr/bin/python

#imports
import os
import sys
import numpy
import copy
import math

outputFileName = "simplex.out"
#helper functions for tableau computations

#other helper functions potentially needed:
# generate tableau from constraints
def tableauGen(m, n, A, B, C):
    #initialize null tableau
    tableau = []
    for i in range(0, m+1):
        nullTableauList = []
        for i in range(0, m+n+1):
            nullTableauList.append(0.0)
        tableau.append(nullTableauList)
    #assign B values in tableau 
    for i in range(0, len(B)):
        tableau[i][len(tableau[i])-1] = B[i]
    #assign C values in tableau
    for i in range(0, len(C)):
        tableau[-1][i] = -C[i]
    #assign A values in tableau
    for row in range(0, m):
        for column in range(0, len(A[row])):
            tableau[row][column] = A[row][column]
    #assign slack variables
    for i in range(0, m):
        for j in range(0, m):
            if (i == j):
                tableau[i][j+n] = 1.0
    """
    print "Generated Tableau:"
    for list in tableau:
        print list
    """
    return tableau

#returns sum of two tableau rows
def addRows(r1, r2):
    rsum = [0 for i in range(len(r1))]
    for i in range (len(r1)):
        rsum[i] = r1[i] + r2[i]
    return rsum

#finds position of either min or max within a row
#exclude last number from search
def findPivotCol(row):
    minNumIndex = 0
    for i in range(0, len(row)):
        if row[i] < row[minNumIndex]:
            minNumIndex = i
    return minNumIndex

#separate function for finding pivot row is necessary. 
#must ignore negative values
def findPivotRow(row):
    minNumIndex = 0
    #start off the search with an absurd number
    # if no number is found at the end of this, then it is unbounded
    minNum = 100000
    for i in range(0, len(row)):
        if (row[i] < minNum and row[i] > 0) or (row[minNumIndex] < 0):
            minNumIndex = i
            minNum = row[minNumIndex]
    #now check if a min number has been found
    if (minNum == 100000):
        file = open(outputFileName, 'w')
        file.write("+inf")
        file.close()
        sys.exit()
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

def checkInt(row):
    isIntSol = "INTEGRAL"
    for i in row:
        #if non-integer is found, then return notInteger
        if math.fabs(i - int(round(i))) > 0.000001:
            print int(round(i))
            print math.fabs(i - int(round(i)))
            print "NONINTEGRAL"
            isIntSol = "NONINTEGRAL"
    return isIntSol

#takes matrix of ratios as input and checks for unbounded
#if unbounded, write "+inf" to output file and exits
def checkUnbounded(row): 
    #check if all pivot column values are negative or zero 
    #use counter to keep track of how many
    invalidNum = 0
    for i in row:
        if i <= 0.0:
            invalidNum = invalidNum + 1
    """
    print row
    print len(row)
    print invalidNum
    """
    if invalidNum == len(row):
        file = open(outputFileName, 'w')
        file.write("+inf") 
        file.close() 
        sys.exit()
    return

#takes B as input, checks for negative val (negative = bounded infeasible)
def checkInfeasible(solRow):
    for i in solRow:
        if i < 0:
            file = open(outputFileName, 'w') 
            file.write("bounded-infeasible")
            file.close()
            sys.exit()
    return

#takes in tableau as input, print ctx & elements of x to file
def getOptSol(tableau, n, m):
    #declare and initialize a list for x values
    xVals = []
    for i in range(0, n):
        xVals.append(0.0)
    #determine which x solution values
    for list in tableau[:-1]:
        for i in range(0, n):
            if list[i] == 1:
                xVals[i] = list[-1]
    #declare and initialize a list of s values
    sVals = []
    for i in range(n, m+n):
        sVals.append(0.0);
    #get remaining s solutions
    for i in range(n, m+n):
        columnVals = []
        for list in tableau:
            columnVals.append(list[i])
        if sum(columnVals) == 1.0:
            for j in range(0, len(columnVals)):
                if columnVals[j] == 1.0:
                    sVals[j] = tableau[j][-1]
                
    #run check for infeasibility on x and s values
    #if any of these are negative, then solution is bounded-infeasible
    checkInfeasible(xVals)
    checkInfeasible(sVals)
    #if not infeasible, print answers
    return xVals

def printOptSol(tableau, xVals):
    file = open(outputFileName, 'w') 
    file.write(str(tableau[-1][-1]) + "\n")
    for x in xVals:
        file.write(str(x) + "\n")
    file.close()
    sys.exit()

def simplex(tableau):
    optSolStat = "SUBOPTIMAL"
    while optSolStat == "SUBOPTIMAL":
        #find pivot index
        pivotCol = findPivotCol(tableau[-1])
        #print pivotCol
        
        #create row of pivot values for unbounded check
        pivotVals = []
        for list in tableau:
            pivotVals.append(list[pivotCol])
        #print "Pivot Column: "
        #print pivotVals

        #check pivot vals for 0 (unbounded solution)
        checkUnbounded(pivotVals)

        #calculate ratios
        ratios = []
        for i in range(0, len(tableau)-1):
            if (pivotVals[i] > 0):
                ratios.append(tableau[i][-1]/pivotVals[i])
            else:
                #append some radical negative number as a placeholder for
                # values that will not result in a valid ratio
                ratios.append(float("-10000"))
        #print "Ratios: "
        #print ratios

        #determine min ratio
        pivotRow = findPivotRow(ratios)
        #print "Pivot row: " 
        #print pivotRow

        #first check coefficient of element at [pivotRow][pivotColumn]
        #  if coefficient is not 1, divide entire row by 1/coeff
        if tableau[pivotRow][pivotCol] != 1.0:
            tableau[pivotRow] = multRow(tableau[pivotRow], 1.0/tableau[pivotRow][pivotCol]) 
            pivotVals[pivotRow] = 1

        for i in range(0, len(tableau)):
            #only perform following operations on rows that are not the pivot row
            if i != pivotRow:
                #determine constant
                multConst =-(pivotVals[i]/pivotVals[pivotRow])

                # multiply pivot row by constant
                tempRow = multRow(tableau[pivotRow], multConst)

                #sum rows, assign new value to proper list position
                tableau[i] = addRows(tableau[i], tempRow)
        """
        print "CURRENT TABLEAU"
        for list in tableau:
            print list

        print "\n"
        """
        #check if new solution is optimal
        optSolStat = checkSol(tableau[-1])
    return optSolStat
        
def compCut(tableau, xVals):
    print "TODO: compute cut and get new constraints"
    #steps:
    #1. compute cut
    #2. obtain new constraints
    #3. append constraints to tableau (then run simplex again)
    return tableau

def main():
    #get arguments, print usage if incorrect
    if (len(sys.argv) != 2):
        print "usage: python assn1.py <filename>"
        sys.exit()

    #set filename, get contents of file and put into list
    filename = sys.argv[1]

    #if filename doesn't exist in the current directory, output error and exit
    if (not(os.path.exists(filename))):
        print "Error: " + filename + " not found"
        sys.exit()

    #otherwise, continue with simplex program
    with open(filename, 'rb') as file:
        inputLines = [row.strip().split() for row in file]

    #convert strings in array to floats
    inputLines = [[float(x) for x in lst] for lst in inputLines]

    #separate input into vars & matrices
    numConstraints = int(inputLines[0][0])
    numVars = int(inputLines[0][1])

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

    tableau = tableauGen(numConstraints, numVars, A, B, C)
    origTableau = copy.deepcopy(tableau)

    #var to track if solution is optimal
    optSolStat = "SUBOPTIMAL" 
    #var to track if solution is integers
    intSolStat = "NONINTEGRAL"
    #initial check to see if solution is optimal 
    #  (for cases where the first solution is actually optimal)
    optSolStat = checkSol(tableau[-1])

    while intSolStat == "NONINTEGRAL":
        #apply simplex algorithm
        while optSolStat != "OPTIMAL":
            optSolStat = simplex(tableau)

        #if optimal solution status is "optimal", check to make sure all are
        #  integers before printing to file
        if optSolStat == "OPTIMAL":
            xVals = getOptSol(tableau, numVars, numConstraints)
            intSolStat = checkInt(xVals)
            #print to file if integral, else perform tableau manip and loop again
            if intSolStat == "INTEGRAL": 
                printOptSol(tableau, xVals)
            else: 
                print "Non integral solutions found"
                #tableau = 
                sys.exit()


if __name__ == "__main__":
    main()

