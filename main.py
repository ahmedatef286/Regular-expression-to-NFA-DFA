###################### vars ######################

operators = ['|' , '.' , '+' , '*' , '(' , ')',]


          

states = []
stateTable = {}

inputs = []
inputString  = "(a.b|c.b)|((a.b.c|x)*.m*)|x.c+"

tempVariables = {}
tempVariablesCounter = 0

stateCounter = 0

###################################################

# get all the inputs in alphabet and make sure all closures are in brackets 
def bracketing():
    global inputs
    global inputString

    i = 0
    while i < len(inputString):
        if inputString[i] not in operators and inputString[i]  not in inputs:
            inputs.append(inputString[i])
        #put closuers in brackets
        if(inputString[i] == '*' or inputString[i] == '+'):
            if(inputString[i-1] != ')'):
                inputString = '('.join( [inputString[ 0 :i-1] , inputString[i-1:len(inputString)]])
                inputString = ')'.join([inputString[0:i+1] , inputString[i+1:len(inputString)]] )
        i += 1

#split regex into parts
def split():
    global tempVariables
    global tempVariablesCounter
    global inputString

    while('(' in inputString):
        lastOpenBracketIndex = 0
        for i in range(0 , len(inputString)):
            if(inputString[i] == '('):
                lastOpenBracketIndex = i
            elif(inputString[i] == ')'):
                        p = ""
                        p = inputString[lastOpenBracketIndex : i+1]
                        tempVariables[tempVariablesCounter] = p
                        
                        inputString = str(tempVariablesCounter).join([inputString[0 :lastOpenBracketIndex], inputString[i+1 : len(inputString)]] )
                        tempVariablesCounter+=1
                        break
    

    

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def main():
    bracketing()
    split()

    print(inputs)
    print(inputString)



    
main()
print(tempVariables)
def handleAnd(expression ):#(a.b.c)
     global stateCounter
     if not has_numbers(inputString= expression):
          tempContainer = []
          tempContainer.append( { 'q'+str(stateCounter) : [[expression[0] ,'q'+str(stateCounter+1) ]]}),
          for i in range(0 , len(expression)):
               if(expression[i] == '.'):
                    tempContainer.append( { 'q'+str(stateCounter+1) : [[expression[i+1] ,'q'+str(stateCounter+2) ]],
                             })
                    stateCounter +=1

          stateCounter+=1
          return tempContainer
                    
def handleOr(expression): #(a|b)
     global stateCounter
     if not has_numbers(inputString= expression):
          tempContainer = []
          for i in range(0 , len(expression)):
               if(expression[i] == '|'):
                    tempContainer.append( { 'q'+str(stateCounter) :[ ['$' ,'q'+str(stateCounter+1) ],['$' ,'q'+str(stateCounter+3) ],],
                            'q'+str(stateCounter+1) : [[expression[i-1] ,'q'+str(stateCounter+2) ]],
                            'q'+str(stateCounter+3) : [[expression[i+1] ,'q'+str(stateCounter+4) ]],
                            'q'+str(stateCounter+2) : [['$' ,'q'+str(stateCounter+5) ]],
                            'q'+str(stateCounter+4) : [['$'  ,'q'+str(stateCounter+5) ]],
                             })
                    stateCounter +=5
          return tempContainer
     
def handleZeroOrMore(expression): #(a)*
     global stateCounter
     if not has_numbers(inputString= expression):
          tempContainer = []
          for i in range(0 , len(expression)):
               if(expression[i] == '*'):
                    tempContainer.append( { 'q'+str(stateCounter) :[ ['$' ,'q'+str(stateCounter+1) ],['$' ,'q'+str(stateCounter+3) ]],
                            'q'+str(stateCounter+1) : [[expression[i-1] ,'q'+str(stateCounter+2) ]],                         
                            'q'+str(stateCounter+2) : [['$' ,'q'+str(stateCounter+1) ], ['$' ,'q'+str(stateCounter+3) ]],
                            
                             })
                    stateCounter +=3
          return tempContainer
def handleOneOrMore(expression): #(a)+
     global stateCounter
     if not has_numbers(inputString= expression):
          tempContainer = []
          for i in range(0 , len(expression)):
               if(expression[i] == '+'):
                    tempContainer.append( { 'q'+str(stateCounter) :[ ['$' ,'q'+str(stateCounter+1) ]],
                            'q'+str(stateCounter+1) : [[expression[i-1] ,'q'+str(stateCounter+2) ]],                         
                            'q'+str(stateCounter+2) : [['$' ,'q'+str(stateCounter+1) ], ['$' ,'q'+str(stateCounter+3) ]],
                            
                             })
                    stateCounter +=3
          return tempContainer
                    
          
          
#lesa me7tageen neshoof taree2a ne3mel join beha

 # "(a.b|c.b)|((a.b.c|x)*.(m)*)|x.(c)+"
print(handleOr('a|b|c'))
     
           
           
     

          

     
     