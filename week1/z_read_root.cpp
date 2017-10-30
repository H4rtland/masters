/* H. Schellman  3-14-99

   example C++ program which reads in pairs of  4-vectors for electrons and
   calculates their invariant mass

*/
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>

#include <math.h> // this gives you math functions like sqrt()

#include "TFile.h"
#include "TH1.h"
#include "TROOT.h" // these are extra root input files for histogramming

using namespace std;

int main() {
    // declare and open the input file
    ifstream inputdata(
        "z.dat"); // create an input stream called inputdata which reads from file "z.dat"

    ofstream outputdata("z.out"); // create a file to store the results you calculate.

    string rootFileName = "z_mass.root";
    TFile *rootOutFile = new TFile(rootFileName.c_str(),
                                   "recreate"); // This is a root file for storing our histograms

    TH1D *z_mass = new TH1D("z_mass", "Z mass ", 50, 50., 150.); // this is a histogram
    // it has a 50 bins, equally spaced between 50 and 100 GeV
    // the z_mass has to be repetated twice
    // a second one with more bins could be called
    TH1D *z_mass_more_bins = new TH1D("z_mass_more_bins", "Z mass ", 100, 50., 150.);
    // it has 100 bins

    // declare variables

    double e1;    // The energy of electron Number 1
    double p1[3]; // Momentum of electron 1
    // this is an array of doubles - it is indexed 0:2, p1[0]  returns contents, p1 is pointer to
    // array
    double e2; // electron 2
    double p2[3];

    // read in the data

    // use a while loop to read in all events. Look at other loops later.
    // data format is px py pz e px py pz e for 2 electrons

    while (inputdata >> p1[0] >> p1[1] >> p1[2] >> e1 >> p2[0] >> p2[1] >> p2[2] >> e2) {

        // sum the 4-vectors

        // need to change this to calculate the mass.
        // Would also like you to calculate the PT of the Z (This should be the sum of its px and
        // py)
        double ez;
        double pz[3];
        ez = e1 + e2;
        for (int j = 0; j < 3; j++) {
            pz[j] = p1[j] + p2[j];
        }

        // calculate the invariant mass and print it

        double temp = ez * ez;
        for (int j = 0; j < 3; j++) {
            temp -= pz[j] * pz[j];
        }

        double mz = sqrt(temp); // use sqrt from the math.h collection
        z_mass->Fill(mz);
        z_mass_more_bins->Fill(mz); // fill the histogram with mz

        // Print the Z_Mass to the screen
        cout << " The Z mass is \t " << mz << endl;

        // Print the z mass to a file
        outputdata << mz << endl;
    }

    rootOutFile->Write();
    rootOutFile->Close();
    return 0; // everyone is happy
}
