from random import random, randint, sample, choice
from Tkinter import *
from time import time
import math

from track_extract_final import extract_track

class dummyDisplay:
    def update(self, position_state):
        pass
    def printdisplay(self):
        pass

    def getdisplay(self):
	pass


class track_space(Frame):
    def __init__(self):
        self.total_cost = 0
	### GUI ELEMENTS
        Frame.__init__(self, 0)
        self.entry = Entry(self)
        self.entry.pack()
        self.doIt = Button(self, text = "submit track", command = self.onEnter)
        self.doIt.pack()
	self.kentry = Entry(self)        
	self.kentry.pack()
	self.text = Text(self)
        self.text.pack()
        self.pack()

    def onEnter(self):
      filename = self.entry.get()
      k = self.kentry.get()
      ### change the one below to support a flag for when to use the other heuristic
      (self.states, self.start, self.display) = extract_track(filename, True)      
      self.focus_state = self.start
      self.restart_heuristic()
      if k!= "":	
	      self.k = int(self.kentry.get()) ### change this one for a second entry box or smthng
	      self.simulate_space_lrtak()
      else:
	      self.simulate_space_lrta()

    
    def restart_heuristic(self):
        for s in self.states:
            s.set_heuristic(0)
    
    ### returns true if all residuals of all states reachable from 
    ### the resulting policy have converged
    def have_residuals_converged(self, epsilon):
        ### if called before setup
        if self.start == None:
            return False

        visited = set([])
        queue = [self.start]
        while len(queue) > 0:
            argmin = queue[0].get_arg_min()
            value = sample(argmin, 1)[0].get_expected_cost()
            if math.fabs(queue[0].h - value)  > epsilon:
                return False
            else:
                visited.add(queue[0])

            queue = queue[1:]

            successors = set([])
            for a in argmin:
                successors.union(set(a.states))
            for s in successors:
                if s not in visited:
                    queue.append(s)
        return True

    def simulate_space_lrta(self): #### LRTA* 
        self.total_cost = 0
	self.focus_state = self.start
	### display managment
        self.display.printdisplay()
	toPrint = self.display.getdisplay()
	self.text.delete(1.0, END)
        self.text.insert(INSERT, toPrint)
        self.text.pack()
        return self.after(100,self.simulate_space_lrta_helper)

    def simulate_space_lrta_helper(self):
        if not self.focus_state.is_goal:
            argmin = self.focus_state.get_arg_min()
            value = sample(argmin, 1)[0].get_expected_cost()
            self.total_cost += sample(argmin,1)[0].cost
            self.focus_state.set_heuristic(value)
            self.focus_state = self.focus_state.move()
            ### display managment
            self.display.update(self.focus_state)
            self.display.printdisplay()    
	    toPrint = self.display.getdisplay()
            self.text.delete(1.0, END)
            self.text.insert(INSERT, toPrint)
            self.text.pack()
            return self.after(100,self.simulate_space_lrta_helper)


    def simulate_space_lrtak(self):

        self.total_cost = 0

	self.focus_state = self.start	

        self.display.printdisplay()

        self.supp = dict([])
        self.stem = dict([])
        for st in self.states:
            self.supp[st] = set([])
            self.stem[st] = set([])

	return self.after(100, self.simulate_space_lrtak_helper)

    def simulate_space_lrtak_helper(self):

        ### start of the loop
        if not self.focus_state.is_goal:
            ### do lookahead routine
            Q = [self.focus_state]
            count = self.k
            while len(Q) > 0 and count > 0:
                v = Q[0]
                Q = Q[1:]
                old_h = v.h ### old heuristic
                argmin = v.get_arg_min()
                new_h = sample(argmin, 1)[0].get_expected_cost() ### new value
                if new_h > old_h:
                    #### some management things
                    for w in self.supp[v]: ### remove v from stems of old supp
                        self.stem[w].remove(v)
                    
                    self.supp[v] = set([]) ### change the supp of v
                    for a in argmin:
                        self.supp[v].union(a.states) ## to all states reachable from actions that are in argmin
                    
                    for w in self.supp[v]:
                        self.stem[w].add(v)

                    ### now we add to the queue 
                    for w in self.stem[v]:
                        if len(self.supp[w]) == 1: ### if supp[w] = {v}
                            Q.append(w)
                            count += -1
                        self.supp[w].remove(v)

                    self.stem[v] = set([])

            ### act
            argmin = self.focus_state.get_arg_min()
            value = sample(argmin, 1)[0].get_expected_cost()
            self.total_cost += sample(argmin,1)[0].cost
            self.focus_state.set_heuristic(value)
            self.focus_state = self.focus_state.move()
            ### display managment
            self.display.update(self.focus_state)
            self.display.printdisplay()    
	    toPrint = self.display.getdisplay()
            self.text.delete(1.0, END)
            self.text.insert(INSERT, toPrint)
            self.text.pack()
            return self.after(100,self.simulate_space_lrtak_helper)
            

    
### start track_space
space = track_space()

### start GUI
space.mainloop()

