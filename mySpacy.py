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
    if not n[1] == 'aux' and not n[1] == 'ROOT':
      return False
    else: return True


def determineIndex(parseList):
    ''' Helper function, determine the position of the object '''
    b = 0
    while parseList[b][1] not in SUBJECTS: b+=1
    e = b
    while parseList[e][1] in SUBJECTS: e+=1
    return (b, e)


def skipSentence(sentence, indicator):
    ''' Called upon those sentence that cannot be converted due to special sturcture they have '''
    return "[" + indicator + "]" + " " + sentence 

def toStatement(sentence, indicator):
    ''' # Convert question sentences to statements # '''
    parseList = parse(sentence)
    # print(parseList) # Debug 
    # Check sentence is convertable 
    if not isProperQuestion(parseList[0]):
      print("WARNNING, Sentence not coverteable, skip this line")
      return skipSentence(sentence, indicator)

    # TODO Handel sentences using 'or' and 'and'
    # Split the sentence into smaller sentences by 'or/and'
    # Determine whether they are complete sentences 
    # Convert each sentence into a statement
    # Merge sentences into one

  
    # Remove the question mark 
    parseList.pop()
    parseList.append((".", "", ""))
    # Convert to basic statement 
    aux = parseList.pop(0)
    indexs = determineIndex(parseList)
    parseList.insert(indexs[1], aux)
    # If expecting positive sentence, return directly
    if indicator.lower() == "yes":
      return listToString(parseList)
    else:
      parseList.insert(indexs[1] + 1, ("NOT", "", ""))
      # TODO double negative 
      dn = indexs[1] + 2
      if parseList[dn][0].lower() == "not":
        parseList.pop(indexs[1] + 1)
        parseList.pop(indexs[1] + 1)
      return listToString(parseList)


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