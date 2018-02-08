/* H. Schellman  3-14-99
   I. Bertram    9/8/2007

   example C++ program which reads in pairs of  4-vectors for electrons and
   calculates their invariant mass

*/

// <- this is a comment, anything to right of this is not a command

#include <fstream>  //
#include <iomanip>  //
#include <iostream> // include a bunch of software libraries to do file reading and writing.
#include <sstream>  //

#include <math.h> // this gives you math functions like sqrt()

using namespace std; // so you do not have to put std:: infornt of every
                     // standard command
                     // allows you to have commands with the same name.

int main() { // main program
    // declare and open the input file
    ifstream inputdata("z.dat"); // create an input stream called inputdata which
                                 // reads from file "z.dat"
                                 // note each line has to end with a ;

    ofstream outputdata("z.out"); // create a file to store the results you calculate.

    // declare variables

    double e1;    // The energy of electron Number 1
    double p1[3]; // Momentum of electron 1
    // this is an array of doubles - it is indexed 0:2, p1[0]  returns contents,
    // p1 is pointer to array
    // p1[0] = px p1[1] = py p1[2] = pz
    double e2; // electron 2
    double p2[3];

    // read in the data

    // use a while loop to read in all events. Look at other loops later.
    // data format is px py pz e px py pz e for 2 electrons
    // keeps reading events until all lines are read in
    // ascii file

    while (inputdata >> p1[0] >> p1[1] >> p1[2] >> e1 >> p2[0] >> p2[1] >> p2[2] >> e2) {

        // sum the 4-vectors

        // need to change this to calculate the mass.
        // Would also like you to calculate the PT of the Z (This should be the
        // sum
        // of its px and py)
        double ez;
        double pz[3];
        ez = e1 + e2;
        for (int j = 0; j < 3; j++) {
            pz[j] = 0.0;
        }

        // calculate the invariant mass and print it

        double temp = ez * ez;
        for (int j = 0; j < 3; j++) {
            temp -= pz[j] * pz[j];
        }

        double mz = sqrt(temp); // use sqrt from the math.h collection

        // Print the Z_Mass to the screen
        cout << " The Z mass is \t " << mz << endl;

        // Print the z mass to a file
        outputdata << mz << endl;
    }
    return 0; // everyone is happy
}
