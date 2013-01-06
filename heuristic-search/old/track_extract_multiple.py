#import sys
#sys.path.append("../")
from landscape import state
from landscape import action
from landscape import structured_space

f = open("ring-1.track")

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

start_state = None

for i in range(width*length):
    l_index = i/width
    w_index = i - l_index*width
    
    if track[l_index][w_index] != 'x':
        s0 = state()
        s1 = state()
        s2 = state()
        

        index_to_states[i] = [s0, s1, s2]
        states_to_indexes[s0] = i
        states_to_indexes[s1] = i
        states_to_indexes[s2] = i
        
        
        if track[l_index][w_index] == "s":
            start_state = s0
            
        if track[l_index][w_index] == "g":
            s0.set_goal()
            s1.set_goal()
            s2.set_goal()
            
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
    a2 = action(1, [1], [t2]) ### stay
    s2.append_action(a1)
    s2.append_action(a2)
    origin_states = [s0, s1, s2]
    target_states = [t0, t1, t2]
    return (origin_states, target_states)
    

for index in index_to_states:
    
    if index - width >= 0:
        ### if square above is in track
        if index - width in index_to_states:    
            upper_states = index_to_states[index-width]
            origin_states = index_to_states[index]                    
            r = connect_track(origin_states, upper_states)
            #index_to_states[index] = r[0]
            #index_to_states[index-width] = r[1]
            
            
        ### if square above is not in track
        else:
            ### it colided with wall, put speed zero
            a = action(1,[1], [index_to_states[index][0]])
            ############################################################################################## missing shit

    if index + width < width*length:
        ### if square below is in track
        if index+width in index_to_states:
            lower_states = index_to_states[index+width]
            origin_states = index_to_states[index]                    
            r = connect_track(origin_states, lower_states)
            #index_to_states[index] = r[0]
            #index_to_states[index-width] = r[1]

        ### if square above is not in track
        else:
            ### it colided with wall, put speed zero
            a = action(1,[1], [index_to_states[index][0]])

    if (index + 1) % width != 0:
        ### if square to right is in track
        if index + 1 in index_to_states:
            right_states = index_to_states[index+1]
            origin_states = index_to_states[index]                    
            r = connect_track(origin_states, right_states)
            #index_to_states[index] = r[0]
            #index_to_states[index-width] = r[1]

        ### if square above is not in track
        else:
            ### it colided with wall, put speed zero
            a = action(1,[1], [index_to_states[index][0]])

    if (index) % width != 0:
        ### if square to left is in track
        if index - 1 in index_to_states:
            left_states = index_to_states[index-1]
            origin_states = index_to_states[index]                    
            r = connect_track(origin_states, left_states)
            #index_to_states[index] = r[0]
            #index_to_states[index-width] = r[1]

        ### if square above is not in track
        else:
            ### it colided with wall, put speed zero
            a = action(1,[1], [index_to_states[index][0]])
            
class trackDisplay:
    def __init__(self, Width, Length):
    ### consider creating an init method
        self.print_board = [["x" for i in range(Width)] for j in range(Length)]

    def update(self, newstate):
        for index in index_to_states:
            char = ' '#str(index_to_states[index].h)
            if newstate in index_to_states[index]:
                char = '0'
            self.print_board[index/length][index-index/length*length] = char

    def printdisplay(self):
        for row in self.print_board:
            line = ""
            for char in row:
                line += char
            print line


t = trackDisplay(width, length)
#print t.print_board
t.update(start_state)
#print t.print_board
#t.printdisplay()

states = []
for states_pack in index_to_states.values():
    states.append(states_pack[0])
    states.append(states_pack[1])
    states.append(states_pack[2])
    
    
space = structured_space(states, start_state)

space.restart_heuristic()

print "number of states"
print len(states)
for s in states:
    if len(s.actions) == 0:
        print 'NOOOOOOOOOO'
        print states_to_indexes[s]
while not space.have_residuals_converged(0.001):
    print space.simulate_space_lrta(start_state, t)


space.restart_heuristic()

while not space.have_residuals_converged(0.001):
    print space.simulate_space_lrtak(90, start_state)#, t)
