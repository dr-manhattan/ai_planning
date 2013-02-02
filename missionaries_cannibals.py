# License: http://opensource.org/licenses/MIT
# complements of Max Kesin

from collections import namedtuple

Side = namedtuple('Side', ['missionaries', 'cannibals', 'destination'])

sideFrom = Side(missionaries=3, cannibals=3, destination=False)
sideTo = Side(missionaries=0, cannibals=0, destination=True)

start_state = (sideFrom, sideTo)


def is_win(state):
    return state[0].destination and state[0].missionaries==3 and state[0].cannibals==3

def dead_side(side):
    return (side.missionaries > 0 #some yummy missionaries to eat
            and side.cannibals > side.missionaries)

def dead_end(state):
    return dead_side(state[0]) or dead_side(state[1])

def boat_trip(state, missionaries, cannibals):
    """ state[0] is always the side with the boat """
    return (
        Side(missionaries=state[1].missionaries+missionaries, 
             cannibals=state[1].cannibals+cannibals,
             destination=state[1].destination),
        Side(missionaries=state[0].missionaries-missionaries, 
             cannibals=state[0].cannibals-cannibals,
             destination=state[0].destination)
        )

tried_states = set([])

def print_state(state):
    if state[0].destination:
        print list(reversed(state))
    else:
        print list(state)
             

def search_trips(state):
    side_from = state[0]
    max_missionaries = min(side_from.missionaries, 2)
    max_cannibals = min(side_from.cannibals, 2)
    for m in range(max_missionaries+1):
        for c in range(max_cannibals+1):
            if m+c > 0 and m+c <= 2:
                new_state = boat_trip(state, m, c)
                if new_state in tried_states: continue
                tried_states.add(new_state)
                if is_win(new_state):
                    print 'win!'
                    print_state(new_state)
                    print 'did m=', m, 'c=', c, 'to side dest=', new_state[0].destination
                    return True
                elif dead_end(new_state):
                    pass #print 'dead_end'
                else:
                    if search_trips(new_state):
                        if new_state[0].destination:
                            print list(reversed(new_state))
                        else:
                            print list(new_state)
                        print 'did m=', m, 'c=', c, 'to side dest=', new_state[0].destination
                        return True
                    else:
                        return False
    
    
search_trips(start_state)
