import turtle


##################################################################################
"""
Functions
"""

# (1) equation checker function
def equationChecker(equation):
    validChars = "ABC+*~"
    for i in range(len(equation)):
        char = equation[i]

        if char not in validChars:
            return False

        elif i > 0 and equation[i].isalpha() and equation[i-1].isalpha(): # checking if there are two
                return False                                              # variables right next to each other

    return True






# (2) deMorgan's Law Function(s)


# (2a)
def deMorgan(equation):
    while "~(" in equation: 
        start = equation.rfind("~(")  #Find the start of notted expression
        end = start + 2  # skips to expression inside
        
        pCount = 1
        while end < len(equation) and pCount > 0:
            if equation[end] == ")":
                pCount -= 1
            if equation[end] == "(":
                pCount += 1
            end += 1 # changing end and tracking to find last parenthesis
        
        subExpr = equation[start+2:end-1]  # get expression inside range
        
        nottedExpr = distributeNOT(subExpr)  

        equation = equation[:start] + nottedExpr + equation[end:]
        
    
    return doubleNegation(equation)  # remove double negations [just in case]



# (2b)
def distributeNOT(expression):
    # applies deMorgan’s Law to an expression inside ~(...)
    newExpr = ""
    i = 0 # initialize "i"
    while i < len(expression):

        
        #print(f"{expression[i]}: char ... {newExpr}: newex ... {expression}: subex")
        if expression[i] == '*':  
            newExpr += '+'
        elif expression[i] == '+':  
            newExpr += '*'
        elif expression[i] == '~':  
            # if there's a "~", check if it there's a variable after it
            if i + 1 < len(expression) and expression[i + 1].isalpha():
                newExpr += expression[i + 1]  # adds just the letter to newExpr
                i += 1 # skips the next character because it's already added
            else:
                newExpr += '~'  # keep tilde if not followed by variable
        elif expression[i].isalpha():  
            newExpr += f"~{expression[i]}"  # apply the "~" to variables without a NOT
        elif expression[i] == '(':
            newExpr += '('
        elif expression[i] == ')':
            newExpr += ')'
        i += 1
    
    
    return doubleNegation(newExpr)



# (2c)
def doubleNegation(expression): # just in case
    while "~~" in expression:
        expression = expression.replace("~~", "")
    return expression

        
    




# (3) : function that creates an nMOS equation

def nmosEqCreator(eq):
    newNmos = "~(" + eq + ")"
    simplifiedNmos = deMorgan(newNmos)
    return simplifiedNmos



# (4): function that creates a pMOS equation
def pmosEqCreator(eq):
    newList = []
    newPmos = ""
    for char in eq:
        newList.append(char)
    for i in range(len(newList)):
        if newList[i].isalpha():
            if i > 0:
                if i-1 == "~":
                    newPmos += newList[i]
                else:
                    newPmos += f"~{newList[i]}"
                    
            elif i == 0:
                    newPmos += f"~{newList[i]}"
        else:
            newPmos += newList[i]

    return doubleNegation(newPmos)
            



# (5): splitting pmos/nmos equations

def splitEq(eq):
    if "+" not in eq:
        return [eq]
    else:
        return eq.split("+")





# (6) turtle functions

##6a: drawing transistors (boxes)

def drawBox(t, x, y, fillColor, label):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor(fillColor)
    t.begin_fill()
    for n in range(4):
        t.forward(20)
        t.left(90)
    t.end_fill()
    t.penup()
    t.goto(x + 30, y + 10)  # label to the right of the box
    t.write(label, align='left', font=('Arial', 12, 'normal'))



##6b: positioning transistors and wires

def drawCircuit(nList, pList):
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    t = turtle.Turtle()
    t.speed(0)  # fastest speed
    #t.hideturtle()  # hide the turtle

    # draw Vcc
    t.penup()
    t.goto(100, 200)
    t.pendown()
    t.write("Vcc", align='left', font=('Arial', 12, 'normal'))





    # draw PMOS 
    xTop = 100
    yTop = 180
    pBranchPoints = []
    
    if len(pList) == 1:
        label = pList[0]
        if '*' in label:  # series
            variables = label.split('*')
            for var in variables:
                drawBox(t, xTop, yTop, 'white', var)
                pBranchPoints.append((xTop + 10, yTop + 10))
                yTop -= 30
        else:  # single variable
            drawBox(t, xTop, yTop, 'white', label)
            pBranchPoints.append((xTop + 10, yTop + 10))
            
            
    elif len(pList) > 1: # multiple ors
        for i, label in enumerate(pList):
            if '*' in label:  # checking if first element is 'anded' (in series)
                variables = label.split('*')
                for var in variables:
                    drawBox(t, xTop + i*50, yTop, 'white', var)
                    pBranchPoints.append((xTop + i*50 + 10, yTop + 10))
                    yTop -= 30
                yTop = 180
            else:
                drawBox(t, xTop + i * 50, yTop, 'white', label)  # Parallel
                pBranchPoints.append((xTop + i * 50 + 10, yTop + 10))





    # draw NMOS
    xBottom = 50
    yBottom = -100
    nBranchPoints = []
    if len(nList) == 1:
        label = nList[0]
        if '*' in label:  # series
            variables = label.split('*')
            for var in variables:
                drawBox(t, xBottom, yBottom, 'black', var)
                nBranchPoints.append((xBottom + 10, yBottom + 10))
                yBottom -= 30
        else:  # single variable
            drawBox(t, xBottom, yBottom, 'black', label)
            nBranchPoints.append((xBottom + 10, yBottom + 10))

            
    elif len(nList) > 1:
        for i, label in enumerate(nList):
            if '*' in label:  # checking if first item is "anded"
                variables = label.split('*')
                for var in variables:
                    drawBox(t, xBottom + i*50, yBottom, 'black', var)
                    nBranchPoints.append((xBottom + i * 50 + 10, yBottom + 10))
                    yBottom -= 30
                yBottom = -100
            else:
                drawBox(t, xBottom + i * 50, yBottom, 'black', label)  # parallel
                nBranchPoints.append((xBottom + i * 50 + 10, yBottom + 10))

    # draw gnd
    t.penup()
    t.goto(75, -175)
    t.pendown()
    t.write("GND", align='left', font=('Arial', 12, 'normal'))

    # connect
    t.penup()
    t.goto(110, 200)  
    t.pendown()
    for point in pBranchPoints:
        t.goto(point[0], point[1])
    t.goto(110, -70)

    t.penup()
    t.goto(110, -150)  # starting at GND
    t.pendown()
    for point in nBranchPoints:
        t.goto(point[0], point[1])
    t.goto(110, -70)

    # draw line to F
    t.penup()
    t.goto(120, -50)
    t.pendown()
    t.forward(100)

    # Draw output label
    t.penup()
    t.goto(230, -50)
    t.write("F", align='left', font=('Arial', 12, 'normal'))

    turtle.done()


        
    
    




################################################################
####################################################################
########################################################################
##################################################################################
"""
Preset variable(s)
"""
IS_VALID_EQ = False


#########################################################################
##################################################################################
#############################################################################

"""
Part 1: user input / solving boolean equation
"""





# prompting user input equation

equation = input("Type in a boolean equation that you would like to see a CMOS transistor circuit \
implementation of.\nHowever:\n\n(1) Do not use more than 2 inputs, and include 1 output. \
\n(2) Make sure to only use 'A', 'B', or 'C' as inputs. The program will use 'F' as the ouput.\n\
(3) Use '+' for 'OR' / '*' for 'AND'. Use '~' before a variable or expression to indicate \
'NOT'.\n(4) Do not include ANY spaces.\n\
(5) You cannot 'NOT'/'AND'/'OR' an entire expression (having more than 1 variable), \
as this program is unable to accept parentheses.\n\
(6) The equation cannot exceed 8 characters.\
\n[i.e. a correctly formatted equation looks like: ~A*B]\n\nType your equation here: ")


# continues asking for an equation until it is valid
while not IS_VALID_EQ:
    if equation == "out":
        break
    elif equationChecker(equation):
        if len(equation) > 8:
           equation = input("Your equation is too long. Try again: ") 
        else:
            IS_VALID_EQ = True
    else:
        equation = input("There was an error with the formatting of your equation. Try again: ")






newEq = equation


########################################################################


"""
Part 2: turning equations into nMos and pMos equations
"""
            

nmosEq = nmosEqCreator(newEq)
print(f"NMOS: {nmosEq}")


pmosEq = pmosEqCreator(newEq)
print(f"PMOS: {pmosEq}")




#########################################################################

"""
Part 3: splitting equations
"""

nSplit = splitEq(nmosEq)
print(nSplit)

pSplit = splitEq(pmosEq)
print(pSplit)



#####################################################################


"""
Part 4: using the drawCircuit function to draw on turtle
"""
   
drawCircuit(nSplit, pSplit)


                
