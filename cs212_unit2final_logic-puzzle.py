"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools
def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    days = (Monday, Tuesday, Wednesday, Thursday, Friday) = (1, 2, 3, 4, 5)
    orderings = list(itertools.permutations(days))

    order = next([Wilkes, Hamming, Minsky, Knuth, Simon]
            for (Wilkes, Hamming, Minsky, Knuth, Simon) in orderings
            if (Knuth - Simon) == 1
            for (designer, programmer, writer, manager, _) in orderings
            if (Knuth - manager) == 1
            and Thursday != designer
            and programmer != Wilkes
            and writer != Minsky
            for (iphone, laptop, droid, tablet, _) in orderings
            if Wednesday == laptop
            and (((programmer,droid) == (Wilkes,Hamming)) or ((droid,programmer) == (Wilkes,Hamming)))
            and ((Knuth != manager) and (tablet != manager))
            and tablet != Friday
            and designer != droid
            and (((laptop,Wilkes) == (Monday,writer)) or ((Wilkes,laptop) == (Monday,writer)))
            and ((iphone == Tuesday) or (tablet == Tuesday))
            )

    names = sorted(zip(order,['Wilkes', 'Hamming', 'Minsky', 'Knuth', 'Simon']))
    return [n[1] for n in names]

print logic_puzzle()