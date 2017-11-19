import spacy 
import codecs
nlp = spacy.load("en")

SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl", "pobj", "prep"]
OBJECTS = ["dobj", "dative", "attr", "oprd"]

def parse(sentence): 
  result = []
  doc = nlp(sentence)
  for token in doc:
    result.append((token.text, token.dep_, token.pos_))
  return result

def isProperQuestion(n):
  if not n[1] == 'aux' and not n[1] == 'ROOT':
    return False
  else:
    return True

def determineIndex(parseList):
  b = 0
  while parseList[b][1] not in SUBJECTS:
    b+=1
  e = b
  while parseList[e][1] in SUBJECTS:
    e += 1
  return (b, e)

def toStatement(sentence, indicator):
  parseList = parse(sentence)
  # print(parseList)
  parseList.pop()
  parseList.append((".", "", "")) 
  aux = parseList.pop(0)
  indexs = determineIndex(parseList)
  parseList.insert(indexs[1], aux)
  if indicator == "yes":
    return parseList
  else:
    parseList.insert(indexs[1] + 1, ("NOT", "", ""))
    return parseList

def listToString(parseList):
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
      print(listToString(toStatement(line, "yes")))
      print(listToString(toStatement(line, "no")))