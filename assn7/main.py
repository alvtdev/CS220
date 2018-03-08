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

def write_line(x, f):
    for item in x:
        f.write(str(item) + " ")
    return

def write_results(legal = False, placement = []):
    #TODO: build output function
    """ output file format:
        - Obj(P,C,L)  D_comm(P,C)  T_mix(P,L)  alpha
            - value of objective function (pos float)
            - total communication distance (pos int)
            - latency improvement (pos float)
            - user-specified param (pos float)

        - n_ops lines describing placement location of each operation
            - input operation: 1  r_in
            - output operation: 2  r_out
            - assay operation (mix): 3  x  y  m  n
                - (x, y) grid coordinate of upper left hand position of mixer
                - (m x n) mixer size
            - other assay operations: t(v)  x  y
                - t(v) pos int type for operation  
                - (x, y) grid coordinate of upper left hand position of mixer
    """
    f = open("placement.out", "w")
    if not legal:
        f.write("No solution found")
    else:
        for l in placement:
            write_line(l, f)
            f.write("\n")
    f.close()

def int_map(x):
    y = []
    for i in range(len(x)):
        y.append(map(int, x[i]))
    return y

def print_list(x):
    for l in x:
        print l
    return


def main(debug = "none"):

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

    # print contents for debugging purposes
    if debug == "arch" or debug == "all":
        print("\nARCH CONTENTS") 
        print("dim_M = " + str(dim_M))
        print("dim_N = " + str(dim_N))
        print("n_input = " + str(n_input))
        print("n_output = " + str(n_output))
        print("n_sensor = " + str(n_sensor))
        print("n_detector = " + str(n_detector))
        print("n_heater = "  + str(n_heater))
        print(inputCoords)
        print(outputCoords)
        print(sensorCoords)
        print(detectorCoords)
        print(heaterCoords)
        print("\n") 

    ################### READ AND SPLIT OPS.IN ###################
    n_assay_ops = 0
    ops_in = read_file("ops.in")
    n_assay_ops = int(ops_in[0][0])
    ops_in = ops_in[1:]
    ops_list = []
    for row in ops_in:
        if row[0] == "3":
            ops_list.append([int(row[0]), float(row[1])])
        else:
            ops_list.append(map(int, row))
    # print contents for debugging purposes
    if debug == "ops" or debug == "all":
        print("n_assay_ops = " + str(n_assay_ops))
        print("ops_list: ")
        print_list(ops_list)

    ################### READ AND SPLIT GRAPHS.IN ###################
    n_ops = 0
    e_int = 0
    e_com = 0
    graphs_in = int_map(read_file("graphs.in"))
    n_ops = graphs_in[0][0]
    e_int = graphs_in[0][1]
    e_com = graphs_in[0][2]
    graphs_in = graphs_in[1:]
    inter_graph = [[0 for x in range(n_ops)] for y in range(n_ops)]
    comm_graph = [[0 for x in range(n_ops)] for y in range(n_ops)]

    # generate interference graph
    if debug == "graphs" or debug == "all":
        print("Generating Interference Graph...")
    for i in range(e_int): 
        # Test output to see which edges were found per graph
        if debug == "graphs" or debug == "all":
            print("Edge from " + str(graphs_in[i][0]) + " to " + str(graphs_in[i][1]))
        tempX = graphs_in[i][0]-1
        tempY = graphs_in[i][1]-1
        inter_graph[tempX][tempY] = 1
        inter_graph[tempY][tempX] = 1
    graphs_in = graphs_in[e_int:]

    # generate communication graph
    if debug == "graphs" or debug == "all":
        print("Generating Communication Graph...")
    for i in range(e_com): 
        if debug == "graphs" or debug == "all":
            print("Edge from " + str(graphs_in[i][0]) + " to " + str(graphs_in[i][1]))
        tempX = graphs_in[i][0]-1
        tempY = graphs_in[i][1]-1
        comm_graph[tempX][tempY] = 1
        comm_graph[tempY][tempX] = 1
    del graphs_in

    # print contents for debugging purposes
    if debug == "graphs" or debug == "all":
        print("\nGRAPHS CONTENTS") 
        print("n_ops = " + str(n_ops))
        print("e_int = " + str(e_int))
        print("e_com = " + str(e_com))
        print("Interference Graph: ")
        print_list(inter_graph)
        print("Communication Graph: ") 
        print_list(comm_graph)
        print("\n")
    
    ################### READ ALPHA.IN ###################
    alpha = float(read_file("alpha.in")[0][0])
    # print contents for debugging purposes
    if debug == "alpha" or debug == "all":
        print("alpha = " + str(alpha))
        print("\n")

    #TODO: Define NSGAII problem given contraints from input files
    ################### NSGA PLACER ###################
    """ Notes:
        - must determine placement of all operations
        - must determine optimal dimensions of each mixing operation
            - mixing operation has sizes of 2x2, 2x3(3x2), 1x4(4x1), 2x4(4x2)
        - start with default NSGAII parameters
        - if a communication link exists between u and v, reduce communication
            cost by placing v near u

        *** Characteristics of a legal solution
        - All assay operations placed within (M-2)x(N-2) subgrid
            -I/O operations are pre-placed on perimeter, cannot be undone
        - For interference edge e = (u,v) in E, u and v cannot overlap
        - Each sensing operation must be placed on electrode with a sensor
        - Each detection operation must be placed on electrode with a detector
        - Each heating operation must be placed on electrode with a heater 
    """


    legal = False # flag to determine if legal solution can be found
    placement = [] # list containing final solution  
    
    
    ################### WRITE RESULTS OUT ###################

    write_results(legal, placement)

    return

if __name__ == "__main__":
    # params to assist with debugging
    if len(sys.argv) > 1 and sys.argv[1].lower() == "debug":
        if len(sys.argv) == 3:
            main(debug = sys.argv[2].lower())
        else:
            main(debug = "all")
    else:
        main()
