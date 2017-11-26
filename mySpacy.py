import spacy
nlp = spacy.load("en")

SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl", "pobj", "prep"]
OBJECTS = ["dobj", "dative", "attr", "oprd"]
QUESTIONMARKS = ['do', 'does', 'did', 'has', 'have', 'is', 'are', 'will']


def parse(sentence):
    ''' Process the sentence using spacy '''
    result = []
    doc = nlp(sentence)
    for token in doc: result.append((token.text, token.dep_))
    return result


def isProperQuestion(n):
    '''Helper function, determine whether the sentence can be converted or not '''
    return n[0].lower() in QUESTIONMARKS


def determineIndex(parseList):
    ''' Helper function, determine the position of the object '''
    b = 0
    while parseList[b][1] not in SUBJECTS and b+1 < len(parseList):
        b+=1
    e = b
    while parseList[e][1] in SUBJECTS and e+1 < len(parseList):
        e+=1
    return (b, e)


def skipSentence(sentence, indicator):
    ''' Called upon those sentence that cannot be converted due to special sturcture they have '''
    return "[" + indicator + "]" + " " + sentence


def checkCC(parseList):
    '''
    Check whether a sentence contains and / or.
    If CC exists, return a list of index of cc.
    Else return an empty list.
    '''
    indexList = []
    for i in range(len(parseList)):
        if parseList[i][1] == "cc":
            indexList.append(i)
    return indexList


def handleCC(parseList, indicator):
    ''' Handle sentences that contains and/or '''
    brkPoints = checkCC(parseList)
    if len(brkPoints) == 0:
        return None # No CC in the sentence.

    ccBin = [] # Temporarily store the cc words
    myBin = [] # Temporarily store splited phrases
    t = []
    result = ""
    ci = 0
    myAnd = ("AND", "", "")
    myOr = ("OR", "", "")

    for i in brkPoints:
        if indicator.lower() == "yes":    ccBin.append(parseList[i])
        else:
            if parseList[i][0].lower() == 'and':    ccBin.append(myOr)
            elif parseList[i][0].lower() == 'or':   ccBin.append(myAnd)

    for a in range(brkPoints[0]):   t.append(parseList[a])
    myBin.append(t)

    for i in range(len(brkPoints)):
        s = brkPoints[i] + 1
        t = []
        while s < len(parseList) and not parseList[s][1] == "cc":
            t.append(parseList[s])
            s+=1
        myBin.append(t)

    for phrase in myBin:
        if not isProperQuestion(phrase[0]):    result += listToString(phrase)
        else:    result += listToString(moveAux(phrase, indicator))

        if ci < len(ccBin):
            result+=ccBin[ci][0] + " "
            ci += 1

    return result

def moveAux(parseList, indicator):
    ''' Move the aux to the proper loaction '''
    aux = parseList.pop(0)
    index = determineIndex(parseList)[1]
    parseList.insert(index, aux)

    if indicator.lower() == "yes":
        return parseList
    else:
        dn = index + 1 # Check double negation
        if parseList[dn][0].lower() == "not":
            parseList.pop(dn)
        else:
            parseList.insert(index + 1, ("NOT", "", ""))
        return parseList


def toStatement(sentence, indicator):
    ''' # Convert question sentences to statements # '''
    parseList = parse(sentence)
    # print(parseList)

    if not isProperQuestion(parseList[0]):
      print("WARNNING, Sentence not coverteable, skip this line")
      return skipSentence(sentence, indicator)

    # Remove puncts
    for token in parseList:
        needReParse = True
        if token[1].lower() in ['punct', 'dep']:
            if token[0].lower() == ">":
                a = parseList.index(token)
                parseList[a] = ('greater', 'amod', 'ADJ')
            elif token[0].lower() == "<":
                a = parseList.index(token)
                parseList[a] =  ('less', 'amod', 'ADJ')
            elif token[0].lower() == "=":
                a = parseList.index(token)
                parseList[a] = ('equal', 'amod', 'ADJ')
            else:
                parseList.remove(token)
                needReParse = False

        if needReParse:    parseList = parse(listToString(parseList))

    # Handel sentences using 'or' and 'and'
    cc = handleCC(parseList, indicator)
    if not cc == None:    return cc

    return listToString(moveAux(parseList, indicator))


def listToString(parseList):
    '''# Convert parseList to String '''
    result = ""
    for t in parseList:    result += t[0] + " "
    return result


if __name__  == '__main__':
    print("==================================================")
    f = open("test.txt", 'r')
    for line in f:
      if not line == "":
        print("==================================================")
        print(line)
        print(toStatement(line, "YES"))
        print(toStatement(line, "NO"))
    print("==================================================")
    appleStr = u"Does Apple hate Google or does Google not hate Apple?"
    apple = toStatement(appleStr, "yes")
    print(apple)
