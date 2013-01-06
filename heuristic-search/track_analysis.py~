### this module implements the analysis of tracks
from track_extract_gui import extract_track
from landscape import structured_space

import os, os.path


def analyze_track(filename, manhattan_heuristic):

	(states, start_state, t) = extract_track(filename, manhattan_heuristic)

	space = structured_space(states, start_state)
	
	results = []
	
	for k in range(1, 4):#len(states)):
		space.restart_heuristic()
	
		lrta_costs = []	

		while not space.have_residuals_converged(0.001):
		    lrta_costs.append(space.simulate_space_lrta(start_state))


		space.restart_heuristic()
	
		lrtak_costs = []

		while not space.have_residuals_converged(0.001):
		    lrtak_costs.append(space.simulate_space_lrtak(k, start_state))

		partial_results = (lrta_costs, lrtak_costs, k)
		
		results.append(partial_results)

	return results

inform_filename = "track_results.csv"

dirtocheck = "./tra"

f = open(inform_filename, "w")

for root, dirs, files in os.walk(dirtocheck):
    for filename in files:
	results = analyze_track(filename, False)      	
	lrta_costs = [sum(partial_results[0]) for partial_results in results]
	lrtak_costs = [sum(partial_results[1]) for partial_results in results]

	### write lrta results	
	f.write("lrta")
	f.write(",")
	f.write(filename)		
	f.write(",")
	for i in range(len(results)):		
		f.write(str(lrta_costs[i]))
		f.write(",")
	f.write("\n")

	### write lrtak results	
	f.write("lrtak")
	f.write(",")
	f.write(filename)		
	f.write(",")
	for i in range(len(results)):		
		f.write(str(lrtak_costs[i]))
		f.write(",")
	f.write("\n")
	
f.close()	


