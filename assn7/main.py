from platypus import NSGAII, DTLZ2
import os
import sys


def read_file(filename):
    print("Reading from " + filename + "...")
    raw_in = []
    f = open(filename, "r")
    for line in f:
        raw_in.append(line.split())
    f.close()
    return raw_in

def int_map(x):
    y = []
    for i in range(len(x)):
        y.append(map(int, x[i]))
    return y

def print_list(x):
    for l in x:
        print l
    return

def main():
    # ARCH.IN - DMFB Variables
    dim_M = 0
    dim_N = 0
    n_input = 0
    n_output = 0
    n_sensor = 0
    n_detector = 0
    n_heater = 0
    inputCoords = []
    outputCoords = []
    sensorCoords = []
    detectorCoords = []
    heaterCoords = []
    ################### READ AND SPLIT ARCH.IN ###################
    arch_in = int_map(read_file("arch.in"))
    dim_M = arch_in[0][0]
    dim_N = arch_in[0][1]
    n_input = arch_in[1][0]
    n_output = arch_in[1][1]
    n_sensor = arch_in[2][0]
    n_detector = arch_in[2][1]
    n_heater = arch_in[2][2]
    print_list(arch_in)
    print dim_M
    print dim_N
    print n_input
    print n_output
    print n_sensor
    print n_detector
    print n_heater
    arch_in = arch_in[3:]
    if n_input > 0:
        inputCoords = arch_in[:n_input]
        arch_in = arch_in[n_input:]
    if n_output > 0:
        outputCoords = arch_in[:n_output]
        arch_in = arch_in[n_output:]
    if n_sensor > 0:
        sensorCoords = arch_in[:n_sensor]
        arch_in = arch_in[n_sensor:]
    if n_detector > 0:
        detectorCoords = arch_in[:n_detector]
        arch_in = arch_in[n_detector:]
    if n_heater > 0:
        heaterCoords = arch_in[:n_heater]
        arch_in = arch_in[n_heater:]
    del arch_in
    print inputCoords
    print outputCoords
    print sensorCoords  
    print detectorCoords
    print heaterCoords
    ################### READ AND SPLIT OPS.IN ###################
    ################### READ AND SPLIT GRAPHS.IN ###################
    n_ops = 0
    e_int = 0
    e_com = 0
    graphs_in = int_map(read_file("graphs.in"))
    n_ops = graphs_in[0][0]
    e_int = graphs_in[0][1]
    e_com = graphs_in[0][2]
    graphs_in = graphs_in[1:]
    print_list(graphs_in)
    print n_ops 
    print e_int
    print e_com
    # TODO: generate graphs

    
    ################### READ ALPHA.IN ###################
    alpha = float(read_file("alpha.in")[0][0])
    print alpha
    return

"""
problem = DTLZ2()
algorithm = NSGAII(problem)
algorithm.run(10000)
#for solution in algorithm.result:
    #print(solution.objectives)

import matplotlib.pyplot as plt

plt.scatter([s.objectives[0] for s in algorithm.result],
        [s.objectives[1] for s in algorithm.result])

plt.xlim([0, 1.1])
plt.ylim([0, 1.1])
plt.xlabel("$f_1(x)$")
plt.ylabel("$f_1(y)$")

plt.show()
"""

if __name__ == "__main__":
    main()
