# Takes in lists and make them even by either:
# 1) Filling them with 'None' values to target length
# 2) Removing the last elements until target length is reached.

def FillNone(*args,**kwargs):
    try:
        target = kwargs['target']
    except:
        print('Unrecognizable target length')
    new_args = []
    for arg in args:
        while len(arg) < target:
            arg.append(None)
        new_args.append(arg)
    return new_args


def RemoveLast(*args,**kwargs):
    try:
        target = kwargs['target']
    except:
        print('Unrecognizable target length')
    new_args = []
    for arg in args:
        while len(arg) > target:
            arg.pop()
        new_args.append(arg)
    return new_args
