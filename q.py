import datetime
import json
from hashlib import md5
import pickle

# d = datetime.date(2015,1,5)

# unixtime = time.mktime(d.timetuple())

class QA:

    def __init__(self, question, answer):
        #self.id = md5(bytes(question, encoding='utf-8')).hexdigest()
        self.question = question
        self.answer   = answer
        
        self.next = datetime.datetime(2021, 1, 1).timestamp()
        self.history = [0,0,0,0,0]
    
    def __repr__(self): 
        a = [self.question, self.answer, self.next, self.history]
        return str(a) #"[% s ][% s]" % (self.question, self.answer)  
    # def __repr__(self):
    #     return str(self)

    # def __str__(self):
    #     return str(self)
        
    # def setQuestion(self, question):
    #     self.question = question
    # def setAnswer(self, answer):
    #     self.answer = answer

    # def setHistory(self, index, value):
    #      self.history[index] = value

    # def setNext(self, next):
    #     self.next = next
    

# questions = []

# questions.append(QA("what do you do?", "nothing"))
# questions.append(QA("que hace tu padre?", "nada"))

# with open("test.txt", "wb") as fp:   #Pickling
#     pickle.dump(questions, fp)

# with open("test.txt", "rb") as fp:   # Unpickling
#     b = pickle.load(fp)

# print(b[0].question)

# print (questions[0].next)
# print ( datetime.datetime.fromtimestamp(questions[0].next) )

# json_string = json.dumps(questions.__dict__)
# json_string = json.dumps([QA.__dict__ for QA in questions])
# json_obj = eval(json_string)
# print(json_obj)
#json_obj[1]['question'] = "aaa"
#print(json_obj[1]['history'][1])
#json_obj['question'].index("what do you do?")
#newList = json.loads(json_string)
#print(type(newList)) # --> list
# [x for x in questions if x.question == "what do you do?"]  # list of all elements with .n==30
# [x for x in newList if x['question'] == "what do you do?"]  # list of all elements with .n==30


# print(questions[1].history)
# questions[1].setHistory(0,10)
# print(questions[1].history)

#print(json_obj[0])

#print(type(json_obj[1]))

Qlist = []

def a(path):
    # contents = repo.get_contents(path, ref=GitHubBranch) 
    # cont = contents.decoded_content.decode()
    cont = "---\ntitle: Feb 9th, 2021\n---\n\n## #flashcard \n### question 1 \n#### answer to 1 \n### question 2 \n#### answer 2\n#### answer 2\n### q3\n#### a3\n##"
    lines = cont.split('\n')
    #print(cont)
    i = 0
    while i <= len(lines) - 1:
        #print(str(i) + " " + lines[i])
        if '#flashcard' in lines[i]:
            flashcardIndent = countIdent(lines[i])
            #print(currentIdent)
            isSub = True
            i = i + 1
            zQ = QA("-1", "")
            while isSub:
                if(i <= len(lines) - 1):
                    if(countIdent(lines[i]) == flashcardIndent + 1):
                        #print(str(i) + " question " + lines[i])
                        #print(countIdent(lines[k]))
                        if(zQ.question != "-1"):
                                Qlist.append(zQ)
                        zQ = QA("", "")
                        zQ.question += lines[i]
                        i += 1
                    elif(countIdent(lines[i]) > flashcardIndent + 1):
                        #print(str(i) + " answer " + lines[i])    
                        zQ.answer += lines[i] 
                        i += 1                
                    else:
                        isSub = False
                        i -= 1
                #print(zQ.question + " ----- " + zQ.answer)
                # if(zQ.question and zQ.answer):
                #     zQ =  QA("", "")
                #print(question + " ----- " + answer)

        i += 1



def countIdent(line):
    sparator = '#'
    count = 0
    while line[count] == sparator:
        if(count == len(line) - 1):
            break

        count += 1    

    return count


a("journals/2021_02_09.md")
print(Qlist)