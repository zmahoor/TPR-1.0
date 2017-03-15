def validPrefix():
    global validColors
    return [ "!"+color[0] for color in validColors]

def isCommand(data):
    global minCommandLength
    global maxCommandLength
    global validColors

    if "http" in data: return False
 
    if (len(data) > maxCommandLength+2 ): return False
    if (len(data) < minCommandLength+2): return False

    if(data.startswith(tuple(validPrefix()))): return True

    return False

def cleanMsg(data):
    data = data.replace("'", '')
    return data

validColors = ['red', 'green', 'blue']
maxCommandLength = 50
minCommandLength = 2


print(isCommand("!rjump"))
print(isCommand("!r"))
print(isCommand("r"))
print(isCommand("adddddddddddddddddddddddddddddddddddddddddddddddddd"))
print(isCommand("r!"))

print(cleanMsg("don't run"))