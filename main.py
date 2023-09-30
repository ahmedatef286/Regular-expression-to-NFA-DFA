###################### vars ######################

operators = ['|' , '.' , '^' , '+' , '*' , '(' , ')',]

states = []
inputs = []

finalTransitions = []

inputString  = "((a|b)|ac|(x|z))*"

# refers to proccessed string
pString = ""

parts = []

###################################################

stateNum = 0
lastSavedState = 0
orTails = []

def AddToTransition(From, key, To):
    tempTransition = []
    tempTransition.append(From)
    tempTransition.append(key)
    tempTransition.append(To)
    return tempTransition

def proccessPart(part, star, plus, orFound):
    global stateNum
    global lastSavedState

    if part == '|':
        orTails.append(stateNum)
        stateNum += 1
        lastSavedState = stateNum
        return


    tempTransitions = []
    Transition = []
    
    if lastSavedState != 0:
        Transition.append(['Q0', '$', 'Q'+str(lastSavedState)])
        lastSavedState = 0

    tempStateNum = 0
    ortest = False

    if orFound:
        orStateNum = stateNum

    if star or plus or orFound:
        tempTransitions.append('Q' + str(stateNum))
        tempTransitions.append('$')
        stateNum += 1
        tempTransitions.append('Q' + str(stateNum))
        Transition.append(tempTransitions)
        tempTransitions = []
        if orFound and star or orFound and plus:
            tempTransitions.append('Q' + str(stateNum))
            tempTransitions.append('$')
            stateNum += 1
            tempTransitions.append('Q' + str(stateNum))
            Transition.append(tempTransitions)
            tempTransitions = []

    thompsonTails = []

    isOR = False
    oneTimeOR = False

    for i in part:
        if i == "|":
            tempTransitions.append("Q"+str(orStateNum))
            isOR = True
            oneTimeOR = True
            tempStateNum = stateNum
            thompsonTails.append(stateNum)
            # stateNum = 0
            ortest = True

        # if it's or the followin 'if' will not work for 1 iteration
        if not isOR:
            tempTransitions.append("Q"+str(stateNum))
        if ortest == True:
            # if there is no 'or' at all it will handle and operations only
            if orFound or plus or star:
                tempTransitions.append("$")
            else:
                tempTransitions.append(i)
            stateNum = tempStateNum
            ortest = False
        else:
            tempTransitions.append(i)
        stateNum += 1
        tempTransitions.append("Q"+str(stateNum))
        Transition.append(tempTransitions)
        tempTransitions = []
        isOR = False
    
    if oneTimeOR:
        thompsonTails.append(stateNum)

    if len(thompsonTails) > 0:
        for i in thompsonTails:
            Transition.append(["Q"+str(i), "$", "Q"+str(stateNum+1)])
    if orFound:
        stateNum += 1

    # make star epsilons
    if star:
        Transition.append(["Q"+str(stateNum), "$", "Q"+str(stateNum+1)])

        Transition.append(["Q"+str(stateNum), "$", "Q"+str(orStateNum+1)])

        Transition.append(["Q"+str(orStateNum), "$", "Q"+str(stateNum+1)])
    # make plus epsilons > same as start but without the skipping epsilon
    elif plus:
        Transition.append(["Q"+str(stateNum), "$", "Q"+str(orStateNum+1)])

        Transition.append(["Q"+str(stateNum), "$", "Q"+str(stateNum+1)])

    return Transition

def compositeTransitions():
    global orTails
    global stateNum
    global finalTransitions
    global parts
    global states

    starFound = False
    plusFound = False
    orFound = False

    for i in parts:
        cleanedPart = i

        if '*' in i:
            starFound = True
            cleanedPart = i.replace('*', '')
        elif '+' in i:
            plusFound = True
            cleanedPart = i.replace('+', '')
        if '|' in i:
            orFound = True

        mainTransition = proccessPart(cleanedPart, starFound, plusFound, orFound)

        starFound = False
        plusFound = False
        orFound = False

        if mainTransition:
            states.append(mainTransition)

    # for loop to put all transitions in a single array (optional for data cleaning)
    for i in range(len(states)):
        for j in range(len(states[i])):
            finalTransitions.append(states[i][j])

    #create the last or tail from the proccessed transitions
    if orTails:
        finalTransitions.append([finalTransitions[len(finalTransitions)-1][2], "$", 'Q'+str(stateNum+1)])

    #create the other or tails
    for i in orTails:
        finalTransitions.append(['Q'+str(i), '$', 'Q'+str(stateNum+1)])

def reverse_clean_TEXT():
    global pString
    tempTEXT = ""
    for i in reversed(range(len(pString))):
        if i != len(pString)-1:
            if pString[i] == pString[i+1] and pString[i] == '-':
                continue
        tempTEXT += pString[i]
    pString = tempTEXT

def processTEXT():
    global inputString
    global pString
    global parts

    oneClosure = False
    bracketClosure = False

    openBracket = False

    for i in reversed(range(len(inputString))):
        if inputString[i] == '*' or inputString[i] == '+':
            if inputString[i - 1] != ')':
                pString += '-'
                pString += inputString[i]
                oneClosure = True
                continue
            else:
                pString += '-'
                pString += inputString[i]
                bracketClosure = True
                continue

        if bracketClosure:
            if inputString[i] == '(':
                pString += '-'
                bracketClosure = False
            elif inputString[i] != ')':
                pString += inputString[i]
            continue

        if oneClosure:
            pString += inputString[i]
            pString += '-'
            oneClosure = False
            continue


        if inputString[i] == ')':
            pString += '-'
            openBracket = True
            continue

        if openBracket:
            if inputString[i] == '(':
                pString += '-'
                openBracket = False
            elif inputString[i] != ')':
                pString += inputString[i]
            continue
        
        if inputString[i] == '|':
            pString += '-'
            pString += inputString[i]
            pString += '-'
            continue

        pString += inputString[i]

    reverse_clean_TEXT()

    # splitting the cleaned text into sequential parts without '' values
    parts = pString.split('-')
    while '' in parts:
        parts.remove('')

def dictionaryTransitions(transitions):
    global inputs
    dictionary = {}
    for transition in transitions:
        dictionary[transition[0]] = []
        dictionary[transition[2]] = []

    for transition in transitions:
        dictionary[transition[0]].append([transition[1] , transition[2]])
        if(transition[1]!= '$' and transition[1] not in inputs):
            inputs.append(transition[1])
    return dictionary


def convertNfaToDfa(NfaDictionary):
    dfaDictionary = {}
    unprocessedItems = []
    #assume that the first state in nfa is always start and last is always end
    startStateInNfa = list(NfaDictionary.keys())[0]
    endStateInNfa = list(NfaDictionary.keys())[-1]

    #create start state for dfa
    startTtempReachableStates = findAllReachableByEpsillion(startStateInNfa , NfaDictionary)
    
    #building dfa table 
    unprocessedItems.append(startTtempReachableStates)
    while len(unprocessedItems) !=0 :
        #initializing the state in dfa dictionary
        currentStateName = produceCompoundStateName(unprocessedItems[0])
        dfaDictionary[currentStateName] = []
        for input in inputs :
            tempReachableStates = []
            for state in unprocessedItems[0]:
                for transition in NfaDictionary[state]:
                    if(transition[0] == input):
                        tempReachableStates.extend( findAllReachableByEpsillion(transition[1] , NfaDictionary))
            if(len(tempReachableStates) != 0):
                #removing duplicates
                tempReachableStates = list(dict.fromkeys(tempReachableStates))
                #putting transition in dfa dictionary
                newStateName = produceCompoundStateName(tempReachableStates)
                dfaDictionary[currentStateName].append([input , newStateName])
                if(tempReachableStates not in unprocessedItems):
                    unprocessedItems.append(tempReachableStates)

            
        unprocessedItems.pop(0)
    return dfaDictionary
            

def produceCompoundStateName(listItems):
    newStateName = ""
    for state in listItems:
        newStateName += state
    return newStateName

def findAllReachableByEpsillion(startState , NfaDictionary):
    #create start state for dfa
    i = 0
    tempReachableStates = [startState]
    currentState = tempReachableStates[i]
    while True:
        for transition in NfaDictionary[currentState] :
            if(transition[0] == '$' and transition[1] not in tempReachableStates):
                tempReachableStates.append(transition[1])
            
        i+= 1
        if(i < len(tempReachableStates)):
            currentState = tempReachableStates[i]
        else:
            break
    return tempReachableStates

         
def main():
    processTEXT()
    compositeTransitions()

    print('\nNFA:\nfinal transitions:\n', finalTransitions)
    print('\nparts of the regex:',parts)
    print("========================================\nDFA:\nRegex:", inputString, "\n")
    print(dictionaryTransitions(finalTransitions))
    print(convertNfaToDfa( dictionaryTransitions(finalTransitions)),"\n")



if __name__ == "__main__":
    
    main()
