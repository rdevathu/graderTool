from importlib.metadata import files
import pandas as pd
import os
import webbrowser

class Student:
    def __init__(self, id, filepath):
        self.id = id
        self.filepath = filepath
        self.grade = 100.0
        self.comments = []
        self.internal = []

    def missQuestion(self, deduction, comment, internal):
        self.grade = self.grade - deduction
        self.comments.append(comment)
        if internal != "":
            self.internal.append(internal)
    
    def printGrade(self):
        print(self.id, print.grade)

def inputChecker(prompt, force = True, isFloat = False):
    inputVal = input(prompt)
    if force:
        while inputVal == "":
            inputVal = input("[ENTER VALUE]\t" + prompt)
    if isFloat:
        while True:
            try:
                inputVal = float(inputVal)
                break
            except ValueError:
                inputVal = input("[WRONG TYPE]\t" + prompt)
                pass

    if isFloat:
        return float(inputVal)
    return inputVal

path = "filesToGrader/"
filesList = os.listdir(path)

studentsList = []

for fileName in filesList:
    if fileName[:4] == "LATE":
        tempStudent = Student(str(fileName[5:15]), fileName)
        studentsList.append(tempStudent)
    else:
        tempStudent = Student(str(fileName[:10]), fileName)
        studentsList.append(tempStudent)

# main loop!
counter = 1
for s in studentsList:
    
    print("\n---", s.id, "({}/{})".format(counter,len(studentsList)), "---")
    webbrowser.open_new_tab(path+s.filepath)
    inputVal = (input("Any errors? (y/N): ") or "n")
    if inputVal == "end":
        s.missQuestion(0, "ENDED HERE", "ENDED HERE")
        break
    while inputVal == "y":
        problemNumber = inputChecker("Problem #: ")
        deductionVal = inputChecker("Deducation: ", isFloat=True)
        commentVal = inputChecker("Comment: ")
        fullComment = "[{}](-{}pts): ".format(problemNumber, deductionVal) + str(commentVal)
        internalVal = inputChecker("Internal: ", force = False)
        s.missQuestion(deductionVal, fullComment, internalVal)
        inputVal = (input("Any errors? (y/N): ") or "n")
    
    counter += 1


gradesDf = pd.DataFrame(columns=['id', 'score', 'comment', 'internal'])

def concatComments(comments):
    commentVal = ''
    for i in range(len(comments)):
        commentVal = commentVal + comments[i]
        if i != len(comments)-1:
            commentVal = commentVal + '\n'
    
    return commentVal


for s in studentsList:
    idVal = s.id
    scoreVal = s.grade
    commentVal = concatComments(s.comments)
    internalVal = concatComments(s.internal)
    
    gradesDf = pd.concat([gradesDf, pd.Series({'id':idVal,
                                'score': scoreVal,
                                'comment': commentVal,
                                'internal': internalVal}).to_frame().T], ignore_index=True)


gradesDf.to_excel("gradesOutput.xlsx")