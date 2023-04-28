# -------------------- Roman to Arabic to Roman number converter -------------------- ##
#Written by: Aarni Junkkala
#Code turns numbers from Roman to Arabic and vice versa.
#Limit of Roman numbers is 3999 -> MMMCMXCIX, can't convert numbers higer than that.

#If you want to call this script from outside, call: Convert(str || int)

class Number: #Creates data of each Arabic and Roman number pair.
    def __init__(self, Roman, Arabic):  
        self.Roman = Roman
        self.Arabic = Arabic
        
Numbers = []

def SetuUpNumbers():
    #Creates a list of class with all number and symbols
    Numbers.append(Number("I",1))
    Numbers.append(Number("V",5))
    Numbers.append(Number("X",10))
    Numbers.append(Number("L",50))
    Numbers.append(Number("C",100))
    Numbers.append(Number("D",500))
    Numbers.append(Number("M",1000))

def RomanToArabic(s):
    global Numbers
    s = str(s)
    s = s.upper() #All to upper so all symbols are same
    #Error check, can't have 4 same symbols in a row
    for i in range(len(s)):
        if i + 3 < len(s):
            if s[i] == s[i + 1] and s[i] == s[i + 2] and s[i] == s[i + 3]:
                return False
        else:
            break

    #Makes a list of all symbols turned into arabian numbers, Example: XIV -> [10,1,5]
    NumberList = []
    for i in range(len(s)):
        for k in range(len(Numbers)):
            if s[i] == Numbers[k].Roman:
                NumberList.append(Numbers[k].Arabic)
                continue
        if len(NumberList) != i + 1:
            return False
    
    #Error check, Numbers are in wrong order.
    #Right: CL -> [100, 50] #Wrong: LC -> [50, 100]
    #Right: XC -> [10, 100] #Right: CX -> [100, 10]
    for i in range(len(NumberList)):
        if i + 1 < len(NumberList):
            if NumberList[i] * 10 < NumberList[i + 1]:
                return False
    
    #Turns numbers into groups that are calculated at the end
    #Example : XCIX -> [[10, 100], [1, 10]]
    #Example2 : CLXV -> [[100], [50], [10], [5]]
    NumberGroups = []
    num = 0
    while num < len(NumberList):
        if num + 1 < len(NumberList):
            if NumberList[num] < NumberList[num + 1]: #Smaller -> IX
                NumberGroups.append([NumberList[num], NumberList[num + 1]])
                num += 2
                continue
            if NumberList[num] >= NumberList[num + 1]: #Greater or equal -> XI || -> XX
                NumberGroups.append([NumberList[num]])
                num += 1
                continue
            if num + 2 < len(NumberList): #if three of same symbol in a row -> VIII
                if NumberList[num] == NumberList[num + 1] and NumberList[num] == NumberList[num + 2]: #Samat 3kpl -> XXX
                    NumberGroups.append([NumberList[num],NumberList[num + 1], NumberList[num + 2]])
                    num += 3
                    continue
                elif NumberList[num] == NumberList[num + 1]: #if two of same symbol in a row -> VII
                    NumberGroups.append([NumberList[num],NumberList[num + 1]])
                    num += 2
                    continue
                    
        else:
            NumberGroups.append([NumberList[num]])
            num += 1
            continue

    #Error check, can't have a group before being lesser than a group after: WRONG: XXC -> [10, 10, 100], RIGHT: CXX ->  [100, 10, 10]
    for i in range(len(NumberGroups)):
        if i + 1 < len(NumberGroups):
            if NumberGroups[i] < NumberGroups[i + 1]:
                return False
            
    #Error check, can't have groub before having a subtraction and then have a next groub being equal of subtraction
    #Example: [[10,100], [10], [1]]. Tens are wrong
    for i in range(len(NumberGroups)):
        if i + 1 < len(NumberGroups):
            if len(NumberGroups[i]) > 1:
                if NumberGroups[i][0] == NumberGroups[i + 1][0]:
                    return False

    #Calculates numbersets. Example: [[10,100], [1,10]] -> [90, 9]
    NumberSets = []
    for i in range(len(NumberGroups)):
        if len(NumberGroups[i]) == 1: #Single number, stays the same
            NumberSets.append(NumberGroups[i][0])
            continue
        if len(NumberGroups[i]) == 2: #Two numbers
            if NumberGroups[i][0] < NumberGroups[i][1]: #if the first number is smaller, then subtrack, first from last
                NumberSets.append(NumberGroups[i][1] - NumberGroups[i][0])
                continue
            if NumberGroups[i][0] >= NumberGroups[i][1]:#if same or higher, just sum up.
                NumberSets.append(NumberGroups[i][0] + NumberGroups[i][1])
                continue
        if len(NumberGroups[i]) == 3: #Three numbers are summed up
            num = 0
            for k in range(len(NumberGroups[i])):
                num += NumberGroups[i][k]
            NumberSets.append(num)
            continue

    Result = 0
    for i in range(len(NumberSets)):
        Result += NumberSets[i]
    return Result

def ArabicToRoman(s):
    s = str(s)
    #Turns arabic symbols into a list
    #Example: 123 -> [1,2,3]
    NumberList = []
    for i in range(len(s)):
        NumberList.append(int(s[len(s) - (i + 1)]))
    NumberList = list(reversed(NumberList))
    
    Result = ""
    #Looks for each conversion of each symbol on numberlist
    for i in range(len(NumberList)):
        Symbol = ""
        if NumberList[i] == 0: #Zero isn't written in roman numbers
            continue
        if NumberList[i] == 9:
            #Adds lowering symbols, example: 9 -> IX, 90 XC, 900 CM
            Symbol = Numbers[(((len(NumberList) - i) - 1) * 2)].Roman
            Result += Symbol
            Symbol = Numbers[(((len(NumberList) - i) - 1) * 2) + 2].Roman
            Result += Symbol
        else: #Rest of the numbers
            ResultHolder = ""
            if NumberList[i] >= 4: #All numbers 4 and above gets first the half symbol (5V,50L,500D)
                Symbol = Numbers[(((len(NumberList) - i) - 1) * 2) + 1].Roman
                ResultHolder += Symbol
                NumberList[i] -= 5 #Reduces the 5 from the number, so rest is worked sameway
                
            if NumberList[i] == -1: #If negative, then needs to have reducing symbol before main symbol
                Symbol = Numbers[(((len(NumberList) - i) - 1) * 2)].Roman
                ResultHolder = Symbol + ResultHolder
                
            if NumberList[i] >= 1: #Adds regular symbols foreach left
                #example: 3 -> III
                #example: 8 -> V (8-5 = 3) -> VIII
                #example: 4 -> V (4-5 = -1) -> IV
                Symbol = Numbers[(((len(NumberList) - i) - 1) * 2)].Roman
                for i in range(NumberList[i]):
                    ResultHolder += Symbol
            Result += ResultHolder
    return Result

def Convert(s):
    s = str(s) #Converts to string, if user inputs argument as an int
    if s == "" or s == None:
        return False

    try:
        s = int(s) #If it can be a integer, then it is arabicnumber
    except:
        s = str(s) #If it can't be an integer, then it must be romannumeral
    
    #Arabic to Roman
    if isinstance(s, int) and s > 0 and s < 4000: #Can't be too high or low
        return ArabicToRoman(s)
    #Roman to Arabic
    if isinstance(s, str):
        s = s.replace(" ", "")
        return RomanToArabic(s)

SetuUpNumbers()
if __name__ == '__main__':
    while True: #Repeats for infinite
        print("--------------------")
        print("Roman to Arabic to Roman number converter")
        UserInput = input("Insert number: ")
        print(Convert(UserInput))