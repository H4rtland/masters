/* H. Schellman  3-14-99

   example C++ program which reads in pairs of  4-vectors for electrons and
   calculates their invariant mass

*/
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>

#include <math.h> // this gives you math functions like sqrt()

#include "TCanvas.h"
#include "TFile.h"
#include "TH1.h"
#include "TPad.h"
#include "TROOT.h" // these are extra root input files for histogramming
#include "TVirtualPad.h"

using namespace std;

int main() {
    // declare and open the input file
    ifstream inputdata("fourVectorsBig.txt"); // create an input stream called inputdata which reads
                                              // from file "z.dat"

    ofstream outputdata("b.out"); // create a file to store the results you calculate.

    string rootFileName = "b_mass.root";
    TFile *rootOutFile = new TFile(rootFileName.c_str(), "recreate"); // This is a root file for storing our histograms
    gPad->Update();
    gPad->SetLogy();

    TH1D *b_mass = new TH1D("b_mass", "B mass ", 50, 0, 20); // this is a histogram
    // it has a 50 bins, equally spaced between 50 and 100 GeV
    // the b_mass has to be repetated twice
    // a second one with more bins could be called
    TH1D *b_mass_more_bins = new TH1D("b_mass_more_bins", "B mass ", 100, 0, 20);
    // it has 100 bins

    // declare variables

    double e1;    // The energy of electron Number 1
    double p1[3]; // Momentum of electron 1
    // this is an array of doubles - it is indexed 0:2, p1[0]  returns contents, p1 is pointer to
    // array
    double e2; // electron 2
    double p2[3];

    double e3;
    double p3[3];

    // read in the data

    // use a while loop to read in all events. Look at other loops later.
    // data format is px py pz e px py pz e for 2 electrons

    while (inputdata >> p1[0] >> p1[1] >> p1[2] >> e1 >> p2[0] >> p2[1] >> p2[2] >> e2 >> p3[0] >> p3[1] >> p3[2] >> e3) {

        // sum the 4-vectors

        // need to change this to calculate the mass.
        // Would also like you to calculate the PT of the Z (This should be the sum of its px and
        // py)
        double eb;
        double pb[3];
        eb = e1 + e2 + e3;
        for (int j = 0; j < 3; j++) {
            pb[j] = p1[j] + p2[j] + p3[j];
        }

        // calculate the invariant mass and print it

        double temp = eb * eb;
        for (int j = 0; j < 3; j++) {
            temp -= pb[j] * pb[j];
        }

        double mb = sqrt(temp); // use sqrt from the math.h collection
        b_mass->Fill(mb);
        b_mass_more_bins->Fill(mb); // fill the histogram with mz

        // Print the b_mass to the screen
        // cout << " The B mass is \t " << mz << endl;

        // Print the z mass to a file
        outputdata << mb << endl;
    }

    rootOutFile->Write();
    rootOutFile->Close();
    return 0; // everyone is happy
}
