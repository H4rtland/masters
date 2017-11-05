#include <iostream>  // this gives you input and output
#include <fstream>   // this gives you  file input and output
#include <math.h>       // this gives you math functions like sqrt()

int main(){
    // declare and open the input file
    std::ifstream inputdata("calculate_mean_2.data");
    
    // declare a double for reading in data
    double xvalue = 0;
    
    //declare mean and width values
    double total = 0;
    double var = 0;
    
    // need to count number of values
    double number=0;
    
    
    while (inputdata >> xvalue ){
        total += xvalue;
        number++;
    }
    
    inputdata.close();
    
    double mean = total/number;
    std::cout << "the mean is : " << mean << " for " << number << " entries" << std::endl;
    
    
    // reopen file
    inputdata.open("calculate_mean_2.data");

    double differences_sum = 0;
    
    // calculate variance here
    while (inputdata >> xvalue ){
        differences_sum += (xvalue-mean)*(xvalue-mean);
    }
    
    double variance_squared = differences_sum/(number-1);
    
    std::cout << "the variance squared is " << variance_squared << std::endl;
    
    return 0;
}
