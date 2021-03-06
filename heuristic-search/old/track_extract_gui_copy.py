from Tkinter import *
from landscape import state
from landscape import action
import math


def extract_track(filename, manhattan_heuristic):
	f = open(filename)

	line = f.readline()
	track = []

	while line != "":
	    line = f.readline()
	    split_line = []
	    for x in line:
		    if x != "\n":
		        split_line.append(x)
	    if len(split_line) != 0:
		track.append(split_line)

	width = len(track[0])
	length = len(track)
	   
	index_to_states = dict([])
	states_to_indexes = dict([])

	goal_indexes = []

	start_state = None

	for i in range(width*length):
	    l_index = i/width
	    w_index = i - l_index*width
	    
	    if track[l_index][w_index] != 'x':
		### zero speed
		s0 = state()
		### up direction
		s1 = state()
		s2 = state()
		### down direction
		s3 = state()
		s4 = state()
		### right direction
		s5 = state()
		s6 = state()
		### left direction		
		s7 = state()
		s8 = state()

		index_to_states[i] = [s0, s1, s2, s3, s4, s5, s6, s7, s8]
		states_to_indexes[s0] = i
		states_to_indexes[s1] = i
		states_to_indexes[s2] = i        
		states_to_indexes[s3] = i
		states_to_indexes[s4] = i
		states_to_indexes[s5] = i
		states_to_indexes[s6] = i
		states_to_indexes[s7] = i
		states_to_indexes[s8] = i
		
		if track[l_index][w_index] == "s":
		    start_state = s0
		    
		if track[l_index][w_index] == "g":
		    s0.set_goal()
		    s1.set_goal()
		    s2.set_goal()
		    s3.set_goal()
		    s4.set_goal()
		    s5.set_goal()
		    s6.set_goal()
		    s7.set_goal()
		    s8.set_goal()
		    goal_indexes.append(i)		
			

	### target_states are 1 step from origin_states		    
	def connect_track(origin_states, target_states):
	    [s0, s1, s2] = origin_states
	    [t0, t1, t2] = target_states
	    ### first s0: possible actions, stay or accelerate
	    a1 = action(1, [1], [s0]) ### stay
	    a2 = action(1, [1], [t1]) ### accelerate
	    s0.append_action(a1)
	    s0.append_action(a2)
	    ### second s1: possible actions, descelerate, stay, or accelerate
	    a1 = action(1, [1], [t0]) ### descelerate
	    a2 = action(1, [1], [t1]) ### stay
	    a3 = action(1, [1], [t2]) ### accelerate
	    s1.append_action(a1)
	    s1.append_action(a2)
	    s1.append_action(a2)
	    ### third s2: possible actions, descelerate, stay
	    a1 = action(1, [1], [t1]) ### descelerate
	    s2.append_action(a1)
	    origin_states = [s0, s1, s2]
	    target_states = [t0, t1, t2]
	    return (origin_states, target_states)
	    
	### target_states are 2 steps from origin_states
	def connect_track_double(origin_states, target_states):
	    [s0, s1, s2] = origin_states
	    [t0, t1, t2] = target_states
	    ### first s0: possible actions, stay or accelerate
	    ### there are no possible actions
	    ### second s1: possible actions, descelerate, stay, or accelerate
	    ### there are no possible actions
	    ### third s2: possible actions, descelerate, stay
	    a1 = action(1, [1], [t1]) ### descelerate
	    a2 = action(1, [1], [t2]) ### stay
	    s2.append_action(a1)
	    s2.append_action(a2)
	    origin_states = [s0, s1, s2]
	    target_states = [t0, t1, t2]
	    return (origin_states, target_states)

	### origin_states with themselves
	def connect_track_break(origin_states):
	    [s0, s1, s2] = origin_states
	    ### all go si -> s0
	    ### first s0
	    a1 = action(.1, [1], [s0]) ### stay
	    s0.append_action(a1)
	    ### second s1
	    a1 = action(.1, [1], [s0]) ### descelerate
	    s1.append_action(a1)
	    ### third s2: possible actions, descelerate, stay
	    a1 = action(.1, [1], [s0]) ### descelerate
	    s2.append_action(a1)
	    origin_states = [s0, s1, s2]
	    return (origin_states, None)



	for index in index_to_states:

	    if index - width >= 0:
		### if square above is in track
		if index - width in index_to_states:    
		    upper_states = index_to_states[index-width]
		    upper_states = upper_states[0:1] + upper_states[1:3]
		    origin_states = index_to_states[index]
		    origin_states = origin_states[0:1] + origin_states[1:3]                    
		    r = connect_track(origin_states, upper_states)

		### if square above is not in track
		else:
		    ### it colided with wall, put speed zero
		    origin_states = index_to_states[index]
		    origin_states = origin_states[0:1] + origin_states[1:3]                    
	            r = connect_track_break(origin_states)
	
		### if 2 squares above is in track		
		if index - 2*width >= 0 and index - 2*width in index_to_states:
		    upper_states = index_to_states[index-width]
		    upper_states = upper_states[0:1] + upper_states[1:3]
		    origin_states = index_to_states[index]                    
		    origin_states = origin_states[0:1] + origin_states[1:3]                    
		    r = connect_track_double(origin_states, upper_states)
					    
	
	    if index + width < width*length:
		### if square below is in track
		if index+width in index_to_states:
		    lower_states = index_to_states[index+width]
		    lower_states = lower_states[0:1] + lower_states[3:5]
		    origin_states = index_to_states[index]            
		    origin_states = origin_states[0:1] + origin_states[3:5]        
		    r = connect_track(origin_states, lower_states)

		### if square above is not in track
		else:
		    ### it colided with wall, put speed zero
		    origin_states = index_to_states[index]
		    origin_states = origin_states[0:1] + origin_states[3:5]        
	            r = connect_track_break(origin_states)

		### if 2 squares below is in track
		if index + 2*width < width*length and index+2*width in index_to_states:
		    lower_states = index_to_states[index+2*width]
		    lower_states = lower_states[0:1] + lower_states[3:5]
		    origin_states = index_to_states[index]                    
		    origin_states = origin_states[0:1] + origin_states[3:5]        
		    r = connect_track_double(origin_states, lower_states)

	    if (index + 1) % width != 0:
		### if square to right is in track
		if index + 1 in index_to_states:
		    right_states = index_to_states[index+1]
		    right_states = right_states[0:1] + right_states[5:7]
		    origin_states = index_to_states[index]              
		    origin_states = origin_states[0:1] + origin_states[5:7]      
		    r = connect_track(origin_states, right_states)

		### if square above is not in track
		else:
		    ### it colided with wall, put speed zero
		    origin_states = index_to_states[index]
		    origin_states = origin_states[0:1] + origin_states[5:7]      
	            r = connect_track_break(origin_states)


		### if 2 squares to right is in track
		if (index + 2) % width != 0 and index + 2 in index_to_states:
		    right_states = index_to_states[index+2]
		    right_states = right_states[0:1] + right_states[5:7]
		    origin_states = index_to_states[index]                    
		    origin_states = origin_states[0:1] + origin_states[5:7]      
		    r = connect_track_double(origin_states, right_states)



	    if (index) % width != 0:
		### if square to left is in track
		if index - 1 in index_to_states:
		    left_states = index_to_states[index-1]
		    left_states = left_states[0:1] + left_states[7:9]
		    origin_states = index_to_states[index]           
		    origin_states = origin_states[0:1] + origin_states[7:9]         
		    r = connect_track(origin_states, left_states)

		### if square above is not in track
		else:
		    ### it colided with wall, put speed zero
		    origin_states = index_to_states[index]
		    origin_states = origin_states[0:1] + origin_states[7:9]         
	            r = connect_track_break(origin_states)

		### if 2 squares to left is in track
		if (index-1) % width != 0 and index - 2 in index_to_states:
		    left_states = index_to_states[index-2]
		    left_states = left_states[0:1] + left_states[7:9]
		    origin_states = index_to_states[index]           
		    origin_states = origin_states[0:1] + origin_states[7:9]                  
		    r = connect_track(origin_states, left_states)

	### object that converts the states of the track and their relations
	### into a string to output in the GUI
	class trackDisplay():
	    def __init__(self, Width, Length, Index_to_states):
		  self.print_board = [["x" for i in range(Width)] for j in range(Length)]
		  self.index_to_states = Index_to_states
	          	  

	    def update(self, newstate):
		for index in self.index_to_states:
		    char = ' ' 
		    if newstate in self.index_to_states[index]:
		        char = '0'
		    self.print_board[(index/width)][index-index/width*width] = char

	    def getdisplay(self):
		toPrint = ""
		for row in self.print_board:
		    line = ""
		    for char in row:
		        line += char
		    toPrint+= line + "\n"
		return toPrint

	    def printdisplay(self):
		print self.getdisplay()
	

	t = trackDisplay(width, length, index_to_states)

	t.update(start_state)

	states = []
	for states_pack in index_to_states.values():
	    states.append(states_pack[0])
	    states.append(states_pack[1])
	    states.append(states_pack[2])
	    states.append(states_pack[3])
	    states.append(states_pack[4])
	    states.append(states_pack[5])
	    states.append(states_pack[6])
	    states.append(states_pack[7])
	    states.append(states_pack[8])
	
	def get_distance_goal(index, goal_i, Width):
	    l_index = index/Width
	    w_index = index - l_index*Width
	    result = float("inf")
	    for goal_index in goal_i:
		gl_index = goal_index/Width
		gw_index = goal_index - gl_index*Width
		distance = math.fabs(gl_index-l_index) + math.fabs(gw_index-w_index)
	    	if distance < result:
			result = distance
	    return result		


	### set up the manhattan heuristic
	if manhattan_heuristic:
		for index in index_to_states:
			states_pack = index_to_states[index]
			distance = get_distance_goal(index, goal_indexes, width)
			states_pack[0].h = distance
			states_pack[1].h = distance
			states_pack[2].h = distance
			states_pack[3].h = distance
			states_pack[4].h = distance
			states_pack[5].h = distance
			states_pack[6].h = distance
			states_pack[7].h = distance
			states_pack[8].h = distance	
	return (states, start_state, t)

