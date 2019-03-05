
# Takes a string as a variable and returns it as a float
def str_to_float(string):
    if type(string) == list:
        for index in range(0, len(string)):
            try:
                string[index] = float(string[index])
            except:
                None

    else:
        string = float(string)

    return string
