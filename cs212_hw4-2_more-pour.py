# -----------------
# User Instructions
# 
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes 
# as input capacities, goal, and (optionally) start. This function should 
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the 
# volume of a glass. 
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i), 
# ('empty', i), ('pour', i, j) where i and j are indices indicating the 
# glass number. 



def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    if start is None:
        start = tuple(0 for c in capacities)

    def pour_goal(state): return goal in state
    
    def pour_successors(state):

        successors = {}
        num_states = range(len(state))
        
        def empty_or_fill(state, glass_idx, level):
            "Given a state, return a new state where the input glass is set to the new level (emptied or filled)."

            def glass_level(i, glass_idx, glass, level):
                "Set the glass matching the glass index to the specified level. Else, return the glass."
                return glass if i != glass_idx and glass != level else level

            return tuple(glass_level(i, glass_idx, state[i], level) for i in num_states)
        
        for i in num_states: # EMPTY AND FILL
            successors[empty_or_fill(state, i, 0)] = ('empty', i)
            successors[empty_or_fill(state, i, capacities[i])] = ('fill', i)
            
            for j in num_states: # POUR (i=glass to pour out, j=glass to pour into)

                # Create a list of states.
                s = list(state)
                
                # Don't pour a glass into itself, or pour an empty glass, or fill a full glass.
                if s[i]==s[j] or s[i]==0 or s[j]==capacities[j]: continue
                
                # Pour out of i as much as will fit in j.
                s[i] = max(0, state[i] - (capacities[j] - state[j]))
                
                # Pour into j as much of i as will fit in j.
                s[j] = min(capacities[j], state[j] + state[i])
                
                # Add the updated pour states into the successors dictionary.
                successors[tuple(glass for glass in s)] = ('pour', i, j)

        return successors

    return shortest_path_search(start, pour_successors, pour_goal)

    
def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ] 
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []
    
print more_pour_problem((1, 2, 4, 8), 4)    

def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)] 
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()