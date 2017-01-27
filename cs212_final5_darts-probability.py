# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def test_darts1():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])
    for total in range(2, 159) + [160, 161, 164, 167, 170]:
        assert valid_out(double_out(total), total)
    for total in [0, 1, 159, 162, 163, 165, 166, 168, 169, 171, 200]:
        assert double_out(total) == None
    return "test_darts1 passes"

def valid_out(darts, total):
    "Does this list of targets achieve the total, and end with a double?"
    return (0 < len(darts) <= 3 and darts[-1].startswith('D')
            and sum(map(value, darts)) == total)

def value(target):
    "The numeric value of a target."
    if target == 'OFF': return 0
    ring, section = target[0], target[1:]
    r = 'OSDT'.index(target[0])
    s = 25 if section == 'B' else int(section)
    return r * s

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I created ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""

# Create constants for ordered list of sections, rings, and ring values.
SECTIONS = "20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5".split()
RINGS = ['OFF', 'D', 'S', 'T', 'S']
RING_VALUES = {'OFF': 0, 'S': 1, 'D': 2, 'T': 3, 'SB': 25, 'DB': 50}

# Get all targets: ['S20',...,'D20',...,T20',...,'OFF']
targets = [r+s for r in 'SDT' for s in SECTIONS] + ['SB', 'DB', 'OFF']

def get_score(t):
    "Get the score of a ring based based on its ring-section values."
    ring = filter(lambda c: c.isalpha(), t)    # 'T20' -> 'T'
    section = filter(lambda c: c.isdigit(), t) # 'T20' -> '20'; 'DB' -> ''
    # Multiply ring by section to get score. If bull, score is bull's ring value.
    return RING_VALUES[ring] * int(section) if section else RING_VALUES[ring]

# Convert targets to a dictionary of {target:score} values.
TARGETS = {t: get_score(t) for t in targets}

# Get possible scores from a single dart throw.
# Sort the scores in reverse order and remove duplicates.
scores = sorted(set(TARGETS.values()), reverse=True)
SCORES = [scores[-1]] + scores[:-1] # Put 0 first: [0, 60, 57, ..., 1]

 
def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    for d1 in SCORES:
        for d2 in SCORES:
            d3 = total - (d1 + d2)
            if d3 in SCORES:
                darts = [name(d1), name(d2), name(d3, double=True)]
                # Return a score only if double out on last dart.
                if darts[-1] != '0':
                    # Remove darts with a value of '0'.
                    return filter(lambda d: d != "0", darts) 

def name(dart, double=False):
    """Get the name of a dart based on its score.
    Loop through target scores and return dart name for first match found.
    """
    for target, score in TARGETS.items():
        if target == 'OFF': continue
        if score == dart and ((double and "D" in target) or not double):
            return target
    return "0"

print test_darts1()

"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ratio (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""

def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    
    # Extract ring and section from target.
    #  'SB' -> ('SB', 'B')
    #  'T20' -> ('T', '20')
    ring, section = (target, 'B') if target.endswith('B') else \
                    (target[0], target[1:])
    
    # Adjust miss rate based on target. Then calculate hit rate.
    #  If target is single ring, reduce miss rate to 1/5.
    #  If target is double bull, triple miss rate, up to a max of 1.0.
    miss = miss/5.0 if ring == 'S' else \
           min(1.0, miss*3.0) if ring == 'DB' else miss
    hit = 1.0 - miss
    
    # Calculate the probabilities of a dart hitting target section and/or ring.
    hit_on_both  = hit * hit            # Hit section and ring.
    hit_on_one   = hit * miss/2.0       # Hit one of section or ring. 1/2 misses to either side.
    miss_on_both = miss/2.0 * miss/2.0  # Missed section and ring.
    miss_DB      = miss/3.0 * hit       # Missed DB section or ring. 1/3 misses to SB.
    miss_SB      = miss/4.0 * hit       # Missed SB section or ring. 1/4 misses to DB.
    
    # Store outcomes as (target, prob) pairs.
    # Targets are any ring-section pairs that are reachable when aiming at the target.
    outcomes = {}
    
    # Bulls-eye probabilities.
    if section == 'B':
        # Probabilities for hitting DB or SB.
        if ring == 'DB':
            outcomes['SB'] = miss_DB
            outcomes['DB'] = hit_on_both
        elif ring == 'SB':
            outcomes['SB'] = hit_on_both
            outcomes['DB'] = miss_SB
        # Remainder of probabilities divided equally among 20 single sections.
        S_prob =  (1.0 - (outcomes['SB'] + outcomes['DB'])) / 20.0
        for s in SECTIONS:
            outcomes['S' + s] = S_prob
    
    # Single, double, and triple probabilities.
    else:
        # Get target and eight neighboring ring-section combinations.
        # 'T20' -> [['S5', 'S20', 'S1'], ['T5', 'T20', 'T1'], ['S5', 'S20', 'S1']] 
        for r in get_regions(ring, RINGS):
            for s in get_regions(section, SECTIONS):
                t = r+s if r != 'OFF' else 'OFF'
                prob = hit_on_both if (t == target) else \
                        hit_on_one if (r==ring or s==section) else \
                        miss_on_both
                if t in outcomes:
                    outcomes[t] += prob
                else:
                    outcomes[t] = prob
    
    return outcomes

def get_regions(target, board):
    """Get the hittable board regions on either side of target.
    The board can be either a list of sections or a list of rings."""
    i = board.index(target)
    return board[i-1], board[i], board[(i+1) % len(board)]

def best_target(miss):
    "Return the target that maximizes the expected score."
    T = {}
    for target in TARGETS:
        if target == 'OFF': continue
        score = 0
        # Get targets and probs for each possible outcome.
        # Multiply each prob by target's score; sum into single score.
        for t, prob in outcome(target, miss).items():
            score += TARGETS[t] * prob
        T[target] = score # Build dict of {target: value} pairs
    return max(T, key=T.get) # Return target with max score.


### TESTING ###

def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016,
             'S11': 0.016, 'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15':
             0.016, 'S14': 0.016, 'S7': 0.016, 'SB': 0.64})
    assert same_outcome(outcome('T20', 0.3),
                        {'S1': 0.045, 'T5': 0.105, 'S5': 0.045,
                         'T1': 0.105, 'S20': 0.21, 'T20': 0.49})
    assert best_target(0.6) == 'T7'
    return "test_darts2 passes"

print test_darts2()