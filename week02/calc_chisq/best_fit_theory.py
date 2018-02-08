import math
import operator

def calc_chi_sq(data_file_name, theory_file_name):
    # Calculate chi_sq/N for a given data file and theory file
    with open(data_file_name, "r") as data_file:
        data = [line for line in data_file.readlines() if not len(line.split()) == 0]
        data = [map(float, d.split()) for d in data]
        data_values, sigmas = zip(*data)

    with open(theory_file_name, "r") as theory_file:
        data = [line for line in theory_file.readlines() if not len(line.split()) == 0]
        theory_values = list(map(float, data))
    
    chi_sq = sum([((theory-data)/sigma)**2
                    for data, sigma, theory in zip(data_values, sigmas, theory_values)])
                    
    return chi_sq/len(data_values)

# Calculate (theory, chi_sq/N) pairs
fits = [(t, calc_chi_sq("calculate_chisq_data.data",
                        "calculate_chisq_theory{0}.data".format(t)))
        for t in range(1, 5)]
        
for theory, chi_sq in fits:
    print "Theory {0}: chi_sq/N = {1}".format(theory, chi_sq)

# Choose theory corresponding to the chi_sq/N closest to 1
best_theory, _ = min([(theory, abs(chi_sq-1)) for theory, chi_sq in fits],
                  key=operator.itemgetter(1))

print "The best theory is theory {0}".format(best_theory)
