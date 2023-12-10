def setvar(name, value):
    '''
    Takes in a 2-character long variable name (string),
    then writes the given value (integer or float)
    to the right spot in settings.txt
    '''
    sets = open("settings.py", "r")
    lines = sets.readlines()
    sets.close()

    news = open("settings.py", "w")
    for line in lines:
        line = line.rstrip()
        if line[:2] == name:
            newline = name+" = "+str(value)
        else:
            newline = line
        news.write(newline+"\n")
    news.close()
