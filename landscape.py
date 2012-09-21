from random import random, randint, sample, choice
from time import time
import math

### return a distribution 
def get_distribution(num_points):
    result = []
    for x in range(num_points):
        result.append(random())
    random_sum = sum(result)    
    result = [x/random_sum for x in result]
    return tuple(result)



### simulate a distribution
### returns a random index of the distribution
def simulate_distribution(distribution):
    breakpoints = [0]
    for i in range(len(distribution)):
        next_point = breakpoints[-1] + distribution[i] 
        breakpoints.append(next_point)
    sample = random()
    for i in range(len(breakpoints)-1):
        if breakpoints[i] <= sample and breakpoints[i+1] > sample:
            return i
    return None



class action:
    def __init__(self, cost, distribution, states):
        self.cost = cost
        self.distribution = distribution
        self.states = states

    def get_next_state(self):
        random_index = simulate_distribution(self.distribution)
        return self.states[random_index]
    
    def get_expected_cost(self): ### return the expected cost to goal
        e_c = self.cost
        for i in range(len(self.states)):
            e_c += self.states[i].h * self.distribution[i]
        return e_c

class state:
    def __init__(self):
        self.actions = []
        self.is_goal = False
    
    def set_goal(self):
        self.is_goal = True    
        self.h = 0

    def set_heuristic(self,h0):
        self.h = h0

    def append_action(self, action):
        self.actions.append(action)
    
    def get_arg_min(self):
        argmin = {}
        best_cost = float('inf')
        for a in self.actions:
            new_cost = a.get_expected_cost()
            if new_cost == best_cost:
                argmin.add(a)
            elif new_cost < best_cost:
                argmin = {a}
                best_cost = new_cost
        return argmin

    def move(self):
        argmin = self.get_arg_min()
        a = sample(argmin, 1)[0]
        return a.get_next_state()


class random_space:
    def __init__(self, num_states):
        self.states = [state() for i in range(num_states)]
        self.start = None

    def generate_random_topology(self, max_degree, max_action_span, is_random_cost, max_goals):
        for s in self.states:
            num_actions = randint(1,max_degree)
            for i in range(num_actions):
               #### generate action's random parameters
               action_span = randint(1, max_action_span)
               action_distribution = get_distribution(action_span)
               if is_random_cost:
                   action_cost = random() 
               else:
                   action_cost = 1
               action_states = sample(self.states, action_span)
               #### initialize action
               a = action(action_cost, action_distribution, action_states)
               #### add action into the state
               s.append_action(a)
            
            s.set_heuristic(0) #### set an initial zero heuristic

        #### set goals:
        num_goals = randint(1, max_goals)
        goal_set = sample(self.states, num_goals)
        for g in goal_set:
            g.set_goal()
    
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

    def simulate_space_lrta(self, s): #### LRTA* 
        ### pick random initial state
        total_cost = 0
        self.start = s

        while not s.is_goal:
            argmin = s.get_arg_min()
            value = sample(argmin, 1)[0].get_expected_cost()
            total_cost += sample(argmin,1)[0].cost
            s.set_heuristic(value)
            s = s.move()
        return total_cost


    def simulate_space_lrtak(self, k, s):
        ### pick random initial state
        total_cost = 0
        
        self.start = s
        
        supp = dict([])
        stem = dict([])
        for st in self.states:
            supp[st] = set([])
            stem[st] = set([])
        ### start of the loop
        while not s.is_goal:
            ### do lookahead routine
            Q = [s]
            count = k
            while len(Q) > 0 and count > 0:
                v = Q[0]
                Q = Q[1:]
                old_h = v.h ### old heuristic
                argmin = v.get_arg_min()
                new_h = sample(argmin, 1)[0].get_expected_cost() ### new value
                if new_h > old_h:
                    #### some management things
                    for w in supp[v]: ### remove v from stems of old supp
                        stem[w].remove(v)
                    
                    supp[v] = set([]) ### change the supp of v
                    for a in argmin:
                        supp[v].union(a.states) ## to all states reachable from actions that are in argmin
                    
                    for w in supp[v]:
                        stem[w].add(v)
                        

                    ### now we add to the queue 
                    for w in stem[v]:
                        if len(supp[w]) == 1: ### if supp[w] = {v}
                            Q.append(w)
                            count += -1
                        supp[w].remove(v)

                    stem[v] = set([])

            ### act
            argmin = s.get_arg_min()
            value = sample(argmin, 1)[0].get_expected_cost()
            total_cost += sample(argmin,1)[0].cost
            s.set_heuristic(value)
            s = s.move()
            #print s.is_goal
        return total_cost

class structured_space(random_space):
    def __init__(self, states, start):
        self.states = states
        self.start = start

#def generate_random_spaces(number_of_spaces):
    


lrta_times = []
lrtak_times = []
lrta_cost = 0
lrtak_cost = 0
lrta_restarts = 0
lrtak_restarts = 0

rs = random_space(1500)
rs.generate_random_topology(19, 50, True, 5)
for i in range(100):
    
    rs.restart_heuristic()

    print i
    start_state_index = choice(range(len(rs.states)))

    start_time = time()
    while not rs.have_residuals_converged(.01):
        start_state = rs.states[start_state_index]
        lrta_cost += rs.simulate_space_lrta(start_state)
        lrta_restarts += 1
    lrta_times.append(time()-start_time)
    
    print "lrta cost"
    print lrta_cost

    rs.restart_heuristic()

    #print "starting lrtak"
    start_time = time()
    while not rs.have_residuals_converged(.01):
        start_state = rs.states[start_state_index]
        lrtak_cost += rs.simulate_space_lrtak(90, start_state)
        #print "restarting lrtak"
        lrtak_restarts += 1
    lrtak_times.append(time() - start_time)
    
    print "lrtak_cost"
    print lrtak_cost

print "#####################################"
print "lrta time"
print sum(lrta_times)/len(lrta_times)
print "lrta cost"
print lrta_cost/len(lrta_times)
print "lrta restarts average"
print lrta_restarts*1.0/len(lrta_times)
print "######################################"
print "lrtak time"
print sum(lrtak_times)/len(lrtak_times)
print "lrtak cost"
print lrtak_cost/len(lrtak_times)
print "lrtak restarts average"
print lrtak_restarts*1.0/len(lrtak_times)
