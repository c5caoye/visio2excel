import codecs
import spacy
nlp = spacy.load("en")

SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl", "pobj", "prep"]
OBJECTS = ["dobj", "dative", "attr", "oprd"]


def parse(sentence):
    ''' Process the sentence using spacy '''
    result = []
    doc = nlp(sentence)
    for token in doc: result.append((token.text, token.dep_, token.pos_))
    return result


def isProperQuestion(n):
    '''Helper function, determine whether the sentence can be converted or not '''
    # if not n[1] == 'aux' and not n[1] == 'ROOT':
    if not n[1] in ['aux', 'ROOT', 'conj']:
      return False
    else: return True


def determineIndex(parseList):
    ''' Helper function, determine the position of the object '''
    b = 0
    while parseList[b][1] not in SUBJECTS and b+1 < len(parseList): b+=1
    e = b
    while parseList[e][1] in SUBJECTS and e+1 < len(parseList): e+=1
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
    # Check cc exists in the list
    brkPoints = checkCC(parseList)
    if len(brkPoints) == 0:
        return None # No CC in the sentence.

    ccBin = []
    for i in brkPoints:
        if indicator.lower() == "yes":
            ccBin.append(parseList[i])
        else:
            if parseList[i][0].lower() == 'and':
                ccBin.append(("OR", "", ""))
            elif parseList[i][0].lower() == 'or':
                ccBin.append(("AND", "", ""))

    myBin = []
    t = []
    for a in range(brkPoints[0]):
        t.append(parseList[a])
    myBin.append(t)
    for i in range(len(brkPoints)):
        s = brkPoints[i] + 1
        t = []
        while s < len(parseList) and not parseList[s][1] == "cc":
            t.append(parseList[s])
            s+=1
        myBin.append(t)
    result = ""
    ci = 0
    for phrase in myBin:
        if not isProperQuestion(phrase[0]):
            result += skipSentence(listToString(phrase), indicator)
        result += listToString(moveAux(phrase, indicator))
        if ci < len(ccBin):
            result+=ccBin[ci][0] + " "
            ci += 1
    return result

def moveAux(parseList, indicator):
    ''' Move the aux to the proper loaction '''
    aux = parseList.pop(0)
    indexs = determineIndex(parseList)
    index = indexs[1]
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
    # Check sentence is convertable
    if not isProperQuestion(parseList[0]):
      print("WARNNING, Sentence not coverteable, skip this line")
      return skipSentence(sentence, indicator)

    # Remove puncts
    for token in parseList:
        if token[1].lower() == "punct":
            parseList.remove(token)

    # Handel sentences using 'or' and 'and'
    cc = handleCC(parseList, indicator)
    if not cc == None:
        return cc

    # Convert to statement according to the indicator
    result = moveAux(parseList, indicator)
    return listToString(result)


def listToString(parseList):
    '''# Convert parseList to String '''
    result = ""
    for t in parseList:
      result += t[0] + " "
    return result

if __name__  == '__main__':
    print("===========")
    f = codecs.open("test.txt", 'r', 'latin-1')
    for line in f:
      if not line == "":
        print("===========")
        print(line)
        print(toStatement(line, "YES"))
        print(toStatement(line, "NO"))
    print("===========")
    tempList = parse(u"Is application not considered verified from GTL perpective or is application overpaid in OSG?")
    # print(tempList)
    handleCC(tempList, "no")
