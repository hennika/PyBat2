# Takes in lists and returns the length of the shortest list
def lists(*args):
    minLength = len(args[0])
    for arg in args:
       if len(arg) < minLength:
           minLength = len(arg)
    return minLength

#Script for testing functions.
#cycles = [1,2,3]
#min = lists(cycles, 'Hei','på', 'deg')
#print (min)