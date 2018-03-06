#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <utility>
#include <vector>
using namespace std;

/* Input file notes:
 * DMFB - "arch.in"
 *      - M and N = DMFB dimensions
 *      - N_input and N_output = number of in/out reservoirs
 *      - N_sensor, N_detector, N_heater 
 *          = number of integrated sensors/detectors/heaters
 *      - N_input lines, ea. line = (x, y) pair for in reservoir location
 *      - N_output lines, ea. line = (x, y) pair for out reservoir location
 *      - N_sensor lines, ea. line = (x, y) pair for sensor locations
 *      - N_detector lines, ea. line = (x, y) pair for detector locations
 *      - N_heater lines, ea. line = (x, y) pair for heater locations
 *      - ASSUME: i/o reservoirs are always on perimeter
 *                all device coords are within rows 2 to M-1, columns 2 to N-1
 * Assay Ops - "ops.in"
 *      - N_ops = number of ops in assay
 *      - N_ops lines, ea. line describes an assay op w/ id #s 1-...-N_ops
 *      - input format: 1 r_in
 *          - r_in = positive integer ID of input reservoir
 *      - output format: 2 r_out
 *          - r_out = positive integer ID of output reservoir
 *      - mixing format: 3 z(v)
 *          - z(v) = cost value, represents importance of mix (FLOAT VALUE)
 *      - other formats: t(v) 
 *          - int type: split = 4, merge = 5, store = 6, sense = 7, detect = 8
 *                      heat = 9
 * Graph file - "graphs.in"
 *      - N_ops, e_int, e_com 
 *          - N_ops = number of assay ops, number of vertices
 *          - e_int = number of edges in interference graph
 *          - e_com = number of edges in communication graph
 *      - e_int lines, enumerate edge set of interference graph
 *          - form: u v
 *      - e_com lines, enumerate edge set of communication graph
 *          - form: u v c(f) 
 *
 * Alpha Parameter File - "alpha.in"
 *      - single floating point value for alpha
 */ 

void printCoords(vector<pair<int,int> > x) {
    for(unsigned i = 0; i < x.size(); i++) {
        cout << "(" << x.at(i).first << ", " << x.at(i).second << ")" << endl;
    }
    return; 
}

void printVec(vector<vector<int> > x) {
    for(unsigned i = 0; i < x.size(); i++) {
        for (unsigned j = 0; j < x.at(i).size(); j++) { 
            cout << x.at(i).at(j) << " ";
        }
        cout << endl;
    }
    return;
}

int main (int argc, char **argv) {

    ifstream inFS;

    //temp vars for pair coord creation
    int tempX = 0;
    int tempY = 0;

    /****************************READ ARCH.IN****************************/
    //DMFB variables
    int dim_M = 0;
    int dim_N = 0;
    int n_input = 0;
    int n_output = 0; 
    int n_sensor = 0;
    int n_detector = 0;
    int n_heater = 0;

    printf("Reading from arch.in... \n");
    inFS.open("arch.in");
    if (!inFS.is_open()) {
        perror("arch.in open failed");
        return EXIT_FAILURE;
    }
    inFS >> dim_M >> dim_N >> n_input >> n_output 
        >> n_sensor >> n_detector >> n_heater;

    cout << "dim_M = " << dim_M << endl;
    cout << "dim_N = " << dim_N << endl;
    cout << "n_input = " << n_input << endl;
    cout << "n_output = " << n_output << endl; 
    cout << "n_sensor = " << n_sensor << endl;
    cout << "n_detector = " << n_detector << endl;
    cout << "n_heater = " << n_heater << endl;

    //input coordinates
    vector<pair<int,int> > inputCoords;
    for(unsigned i = 0; i < n_input; i++) {
        inFS >> tempX >> tempY;
        inputCoords.push_back(make_pair(tempX, tempY));
    }
    cout << "Input Coords: " << endl;
    printCoords(inputCoords);

    //output coordinates
    vector<pair<int,int> > outputCoords;
    for(unsigned i = 0; i < n_input; i++) {
        inFS >> tempX >> tempY;
        outputCoords.push_back(make_pair(tempX, tempY));
    }
    cout << "Output Coords: " << endl;
    printCoords(outputCoords);

    //sensor coordinates
    vector<pair<int,int> > sensorCoords;
    for(unsigned i = 0; i < n_input; i++) {
        inFS >> tempX >> tempY;
        sensorCoords.push_back(make_pair(tempX, tempY));
    }
    cout << "Sensor Coords: " << endl;
    printCoords(sensorCoords);

    //detector coordinates
    vector<pair<int,int> > detectorCoords;
    for(unsigned i = 0; i < n_input; i++) {
        inFS >> tempX >> tempY;
        detectorCoords.push_back(make_pair(tempX, tempY));
    }
    cout << "Detector Coords: " << endl;
    printCoords(detectorCoords);
    
    //heater coordinates
    vector<pair<int,int> > heaterCoords;
    for(unsigned i = 0; i < n_input; i++) {
        inFS >> tempX >> tempY;
        heaterCoords.push_back(make_pair(tempX, tempY));
    }
    cout << "Heater Coords: " << endl;
    printCoords(heaterCoords);
    inFS.close();

    /****************************READ OPS.IN****************************/
    //Assay Ops Variables
    int n_assay_ops = 0;
    float mix_importance = 0.0; 
    vector<int> ops;

    printf("\nReading from ops.in... \n");
    cout << "TODO: COMPLETE ASSAY OPS" << endl;
    inFS.open("ops.in");
    if (!inFS.is_open()) {
        perror("ops.in open failed");
        return EXIT_FAILURE;
    }
    inFS >> n_assay_ops;
    cout << "n_assay_ops = " << n_assay_ops << endl;
    for(unsigned i = 0; i < n_assay_ops; i++) {
    }
 /* Assay Ops - "ops.in"
 *      - N_ops = number of ops in assay
 *      - N_ops lines, ea. line describes an assay op w/ id #s 1-...-N_ops
 *      - input format: 1 r_in
 *          - r_in = positive integer ID of input reservoir
 *      - output format: 2 r_out
 *          - r_out = positive integer ID of output reservoir
 *      - mixing format: 3 z(v)
 *          - z(v) = cost value, represents importance of mix (FLOAT VALUE)
 *      - other formats: t(v) 
 *          - int type: split = 4, merge = 5, store = 6, sense = 7, detect = 8
 *                      heat = 9
 */
    //fill vars
    inFS.close(); 

    /****************************READ GRAPHS.IN****************************/
    //Graph Variables
    int n_ops = 0;
    int e_int = 0;
    int e_com = 0;
    printf("\nReading from graphs.in... \n");
    inFS.open("graphs.in");
    if (!inFS.is_open()) {
        perror("graphs.in open failed");
        return EXIT_FAILURE;
    }
    inFS >> n_ops >> e_int >> e_com;

    //generate matrix representation of interference graph
    cout << "\nGenerating Interference Graph: " << endl;
    vector<vector<int> > interGraph(n_ops, vector<int> (n_ops));
    for(unsigned i = 0; i < e_int; i++) {
        inFS >> tempX >> tempY;
        cout << "Edge from " << tempX << " to " << tempY << endl;
        interGraph.at(tempX-1).at(tempY-1) = 1;
        interGraph.at(tempY-1).at(tempX-1) = 1;
    }
    printVec(interGraph);

    //generate matrix representation of communication graph
    cout << "\nGenerating Communication Graph: " << endl;
    vector<vector<int> > commGraph(n_ops, vector<int> (n_ops));
    for(unsigned i = 0; i < e_com; i++) { 
        inFS >> tempX >> tempY;
        cout << "Edge from " << tempX << " to " << tempY << endl;
        commGraph.at(tempX-1).at(tempY-1) = 1;
        commGraph.at(tempY-1).at(tempX-1) = 1;
    }
    printVec(commGraph);

    inFS.close();

    float alpha = 0.0;
    /****************************READ ALPHA.IN****************************/
    printf("\nReading from alpha.in... \n");
    inFS.open("alpha.in");
    if (!inFS.is_open()) {
        perror("alpha.in open failed");
        return EXIT_FAILURE;
    }
    inFS >> alpha; 
    cout << "alpha = " << alpha << endl;
    inFS.close();

    /****************************BEGIN PLACEMENT****************************/
    vector<vector<int> > solGrid(dim_M, vector<int> (dim_N));

    return 0;
}
