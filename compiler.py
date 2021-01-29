############# Compailers second stage: middle code//symbol matrix//meaning analyse ############
####### team: Iliana Vlaxou with AM:2411 and username:cse32411
#######       Spuros Tsotzolas with AM:3099 and username:cse53099


import sys
import os # for delete file

# keep our stadard words
keyWords = ['program','endprogram','declare','if','then','else','endif',
'while','endwhile','dowhile','enddowhile','loop','endloop','exit','forcase','endforcase',
'incase','endincase','when','default','enddefault','function','endfunction',
'return','in','inout','inandout','and','or','not','input','print']

strr = ""        # here will be copied the starlet file

pos = 0
line = 1         # position and line in starlet file

tokenID = []

###@global values for middle and c code###
clabel=0              # here we keep the number of label in c code
labelcounter = 0      # here we keep the number of label in middle code
quads = []            # list of quads in middle code
varcounter = 0        # counter of my temporary variables
exitList = []
Cquads=[]             # list of quads in c code
exitListC=[]
numExit = 0

#add_oper
addPlace = ''

#mul_oper
mulOperPlace = ''

#optional_sign
optionalsignPlace = ''

#relational_oper
relationOperPlace = ''

#factor
factorPlace = ''

#assigmentStat
assigmentStatPlace=''

#expression
expressionPlace = ''

#idtail
idtailPlace = ''

#term
termPlace = ''

####false and true lists from functions####
#condition
condTrue = []
condFalse = []
condTrueC=[]
condFalseC=[]

#boolterm
booltermFalse = []
booltermTrue = []
booltermTrueC = []
booltermFalseC = []

#boolfactor
boolfactorTrue = []
boolfactorFalse = []
boolfactorTrueC = []
boolfactorFalseC = []

####@Global values using for symbol matrix####
nestingLevel = 1
offset = 12
firstquad = 0
entity = []
scope = []
nameFunc = ''
entertoScopeNow = False

###files which are used###
f = open(sys.argv[1], 'r')
strr = f.read()
f.close()

f1 = open("test.int","w+")
f2 = open("test.c","w+")
f3 = open("test.asm","w+")    # the lines of this file will be coppied to f4 and after it will be deleted
f3.write("L:\n")
f3.write("    j Lmain\n")
f4 = open("file.asm","w+")

###########################
#functions for middle and c code #
###########################

def nextquad(): # return the number of the next quadruple
	global labelcounter

	next = labelcounter + 1
	return next


def genquad(op, x, y, z ): #create the next quadruple at the next label
    global labelcounter
    global quads

    quads.append([str(nextquad()), op, x, y, z])
    labelcounter += 1


def newTemp():  # return the last temp var that i create
    global varcounter

    t = ""
    t = "t_" + str(varcounter) #for t_0 or t_1 ...
    varcounter += 1
    return t


def emptylist(): # create an emptylist
	return []


def makelist(x): # create a list with x inside
    return [x]


def mergelist(x,y): # unit two list , x list has inside the y list
    x += y
    return x


labelList = []  #  here we keep same labels that we will need for the assemble code
loopLabels = [] #                             //
ifList = []     #                            //
def backpatch (x, y):
    global quads
    global labelList
    global exitlist
    global exitList
    global ifList
    global numExit

    for i in range (0, len(x)):
        label = x[i]
        for j in range (0, len(quads)):
            labelQuad = quads[j][0]
            if labelQuad == str(label):
                quads[j][4] = str(y)
                if(x==exitlist):
                    loopLabels.append(quads[j][4])
                elif(len(exitList)!=0 and x==exitList[numExit-1]):
                    ifList.append(quads[j][4])
                else:
                    labelList.append(quads[j][4])
                break

def Cgenquad(op, x, y, z ): #create the next quadruple at the next label in c code
	global clabel
	global Cquads

	clabel+=1
	Cquads.append([str(clabel), op, x, y, z, ';'])

def Cbackpatch (x, y):
    global Cquads

    for i in range (0, len(x)):
        Clabel = x[i]
        for j in range (0, len(Cquads)):
            ClabelQuad = Cquads[j][0]
            if ClabelQuad == str(Clabel):
                Cquads[j][4] = str(y)
                break


#lectical analyse
def lex():
    global strr
    global line
    global pos
    closed_comments = True
    limitOfLetters = 0   # only the 30 first letters take care of
    state = 0
    char = ""
    word = ""

    while(True):
        if(pos < len(strr)):
            if(strr[pos] == '\n'):
                line+=1
            char = strr[pos]
            pos+=1

        else:
            char = 'EOF'

        while(True):
            if(char=='EOF' and closed_comments):
                word = char
                return [word, 'EOFtk']

            elif(state==0 and char.isspace()):      # ignore the spaces
                state = 0
                break

            elif(state==0 and char.isalpha()):
                state = 1
                word = char
                limitOfLetters += 1
                break

            elif(state==0 and char.isdigit()):
                state = 2
                word = char
                break

            elif(state==0 and char=='+'):
                word = char
                return [word, '+tk']

            elif(state==0 and char=='-'):
                word = char
                return [word, '-tk']

            elif(state==0 and char=='*'):
                word = char
                return [word, '*tk']

            elif(state==0 and char=='='):
                word = char
                return [word, '=tk']


            elif(state==0 and char=='<'):
                state = 3
                word = char
                break

            elif(state==0 and char=='>'):
                state = 4
                word = char
                break

            elif(state==0 and char==':'):
                state = 5
                word = char
                break

            elif(state==0 and char=='/'):
                state = 6
                break

            elif(state==0 and char==';'):
                word = char
                return [word, ';tk']

            elif(state==0 and char==','):
                word = char
                return [word, ',tk']

            elif(state==0 and char=='('):
                word = char
                return [word, '(tk']

            elif(state==0 and char==')'):
                word = char
                return [word, ')tk']

            elif(state==0 and char=='['):
                word = char
                return [word, '[tk']

            elif(state==0 and char==']'):
                word = char
                return [word, ']tk']

            elif(state==1 and (char.isalpha() or char.isdigit())):
                state = 1
                if(limitOfLetters < 30):
                    word += char
                    limitOfLetters += 1
                break

            elif(state==1 and not(char.isalpha() or char.isdigit())):          # recognize and go a positiion back (check if line must also be reduced)
                pos-=1
                if(strr[pos]=='\n'):
                    line-=1
                if(word in keyWords):
                    return [word, word + 'tk']
                else:
                    return [word, 'idtk']

            elif(state==2 and char.isdigit()):
                state = 2
                word+=char
                break

            elif(state==2 and not char.isdigit()):
                if(char.isalpha()):
                    print('Error: The constants must consist only of digits... found in line:', line)
                    exit()

                elif(int(word)>32767):
                    print('Error: You did not give valid number... found in line:', line)
                    exit()

                pos-=1
                if(strr[pos]=='\n'):
                    line-=1
                return [word, 'constanttk']

            elif(state==3):
                if(char=='='):
                    word+=char
                    return [word, '<=tk']

                elif(char=='>'):
                    word+=char
                    return [word, '<>tk']
                else:
                    pos-=1
                    if(strr[pos]=='\n'):
                        line-=1
                    return [word, '<tk']

            elif(state==4):
                if(char=='='):
                    word+=char
                    return [word, '>=tk']

                else:
                    pos-=1
                    if(strr[pos]=='\n'):
                        line-=1
                    return [word, '>tk']

            elif(state==5):
                if(char=='='):
                    word+=char
                    return [word, ':=tk']

                else:
                    pos-=1
                    if(strr[pos]=='\n'):
                        line-=1
                    return [word, ':tk']

            elif(state==6):
                if(char=='/'):              # comments with "//"
                    state = 7
                    closed_comments = False
                    break

                elif(char=='*'):            # comments with "/*"
                    state = 8
                    closed_comments = False
                    break

                else:
                    pos-=1
                    if(strr[pos]=='\n'):
                        line-=1
                    word = '/'
                    return [word, '/tk']

            elif(state==8):
                if(char=='EOF'):
                    print('Error: opened comments is not closed')
                    exit()

                elif(char=='*'):
                    state = 9
                    break

                elif(char=='/'):
                    state = 10
                    break

                else:
                    state = 8
                    break

            elif(state==9):
                if(char=='/'):              # the comments be closed... move to state 0
                    state = 0
                    closed_comments = True
                    break

                else:
                    state = 8
                    break

            elif(state==10):
                if(char=='*' or char=='/'):
                    print('Error: You opened second time comments without closed the first... found in line:', line)
                    exit()

                else:
                    state = 8
                    break

            elif(state==7):
                if(char=='\n'):
                    state = 0
                    break
                elif(char=='/'):
                    state = 11
                    break

                else:
                    state = 7
                    break

            elif(state==11):
                if(char=='\n'):
                    state = 0
                    break
                elif(char=='/' or char=='*'):
                    print('Error: You opened second time comments without closed the first... found in line:', line)
                    exit()
                else:
                    state = 7
                    break

            else:
                print('Error: not valid elements... line:', line)
                exit()




#systax analyse
def optionalSign():
    global tokenID
    global optionalsignPlace
    global addPlace

    if(tokenID[1]=='+tk' or tokenID[1]=='-tk'):
        addOper()
        optionalsignPlace = addPlace
    else:
        optionalsignPlace = ''


def mulOper():
    global tokenID
    global mulOperPlace

    if(tokenID[1]=='*tk'):
        mulOperPlace = tokenID[0]
        tokenID = lex()
    elif(tokenID[1]=='/tk'):
        mulOperPlace = tokenID[0]
        tokenID = lex()
    else:
        print('SYntax error: A "/" or "*" was expected in line:', line)
        exit()


def addOper():
    global tokenID
    global addPlace

    if(tokenID[1]=='+tk'):
        addPlace = tokenID[0]
        tokenID = lex()
    elif(tokenID[1]=='-tk'):
        addPlace = tokenID[0]
        tokenID = lex()
    else:
        print('Syntax error: A "+" or "-" was expected in line:', line)
        exit()


def relationalOper():
    global tokenID
    global relationOperPlace

    if(tokenID[1]=='=tk'):
        relationOperPlace = tokenID[0]
        tokenID = lex()
    elif(tokenID[1]=='<=tk'):
        relationOperPlace = tokenID[0]
        tokenID = lex()
    elif(tokenID[1]=='>=tk'):
        relationOperPlace = tokenID[0]
        tokenID = lex()
    elif(tokenID[1]=='>tk'):
        relationOperPlace = tokenID[0]
        tokenID = lex()
    elif(tokenID[1]=='<tk'):
        relationOperPlace = tokenID[0]
        tokenID = lex()
    elif(tokenID[1]=='<>tk'):
        relationOperPlace = tokenID[0]
        tokenID = lex()
    else:
        print('Syntax Error: A "=" or "<=" or ">=" or "<" or ">" or "<>" was expected in line:', line)
        exit()

levelCaller = 0    # here we keep the nestingLevel of caller function
def idtail():
    global tokenID
    global assigmentStatPlace
    global factorPlace
    global idtailPlace
    global frCallee
    global fqCallee
    global caller
    global levelCaller
    global levelOfEntity
    global offsetOfEntity

    if(tokenID[1]=='(tk'):
        calfactorPlace = factorPlace     # in calfactorPlace local variable we keep the name of function which is called
        frCalleeAndFindCalller(calfactorPlace)
        searchEntity(caller)
        levelCaller = levelOfEntity
        actualpars()
        ###middle code###
        idtailPlace = newTemp()
        genquad('par', idtailPlace, 'RET', '')
        f3.write("L" + str(labelcounter) + ":\n")
        genquad('call', calfactorPlace, ' ', ' ')
        ########################
        newEntity(idtailPlace, 'temp')
        searchEntity(idtailPlace)
        f3.write("    add $t0, $sp, -" + str(offsetOfEntity) + "\n")
        f3.write("    sw $t0, -8($fp)\n")
        searchEntity(calfactorPlace)
        f3.write("L" + str(labelcounter) + ":\n")
        if(levelOfEntity==levelCaller):
            f3.write("    lw $t0, -4($sp)\n")
            f3.write("    sw $t0, -4($fp)\n")
        elif(levelOfEntity!=levelCaller):
            f3.write("    sw $sp, -4($fp)\n")
        f3.write("    add $sp, $sp, " + str(frCallee) + "\n")
        f3.write("    jal L" + str(fqCallee) + "\n")
        f3.write("    add $sp, $sp, -" + str(frCallee) + "\n")
    else:
        idtailPlace = factorPlace



def factor():
    global tokenID
    global factorPlace
    global expressionPlace

    if(tokenID[1]=='constanttk'):
        ########################
        factorPlace = tokenID[0]  ###middle code {p1}
        ########################
        tokenID = lex()
    elif(tokenID[1]=='(tk'):
        tokenID = lex()
        expression()
        ##########################
        factorPlace = expressionPlace ###middle code {p2}
        ##########################
        searchEntity(factorPlace)
        if(tokenID[1]==')tk'):
	        tokenID = lex()
        else:
	        print('Syntax error: A ")"  was expected in line:', line)
	        exit()
    elif(tokenID[1]=='idtk'):
        searchEntity(tokenID[0])
        factorPlace = tokenID[0]
        tokenID = lex()
        idtail()
        #########################
        factorPlace = idtailPlace         ###middle code {p3}
        #########################

    else:
        print('Syntax error: A "constant" or a "(" or a "id" was expected in line:', line)
        exit()


def term():
    global tokenID
    global factorPlace
    global mulOperPlace
    global termPlace
    global expByPar
    global labelcounter

    factor()
    #####################
    f1 = factorPlace ###middle code {p1}
    res = f1
    #####################
    while(tokenID[1]=='*tk' or tokenID[1]=='/tk'):
        mulOper()
        factor()
        #########middle code {p2} and assemble code for *|/#########
        f2 = factorPlace
        res = newTemp()
        newEntity(res, 'temp')
        genquad(mulOperPlace, f1, f2, res)
        if(expByPar==False):
            f3.write("L" + str(labelcounter) + ":\n")
        else:
            labelcounter -= 1
        if(mulOperPlace=='*'):
            loadvr(f1,1)
            loadvr(f2,2)
            f3.write("    mul $t1, $t1, $t2\n")
            storerv(1,res)
        elif(mulOperPlace=='/'):
            loadvr(f1,1)
            loadvr(f2,2)
            f3.write("    div $t1, $t1, $t2\n")
            storerv(1,res)
        Cgenquad(res,'=',f1+mulOperPlace,f2)
        f1 = res
        #########################################
    termPlace = res



def expression():
    global tokenID
    global termPlace
    global optionalsignPlace
    global expressionPlace
    global expByPar
    global labelcounter

    optionalSign()
    term()
    ##################
    t1 = optionalsignPlace + termPlace  ###middle code {p1}
    res = t1
    ##################
    while(tokenID[1]=='+tk' or tokenID[1]=='-tk'):
        addOper()
        term()
        #########middle code {p2} and assemble code for +|-#########
        res = newTemp()
        newEntity(res, 'temp')
        genquad(addPlace, t1, termPlace, res)
        if(expByPar==False):
            f3.write("L" + str(labelcounter) + ":\n")
        else:
            labelcounter -= 1
        if(addPlace=='+'):
            loadvr(t1,1)
            loadvr(termPlace,2)
            f3.write("    add $t1, $t1, $t2\n")
            storerv(1,res)
        elif(addPlace=='-'):
            loadvr(t1,1)
            loadvr(termPlace,2)
            f3.write("    sub $t1, $t1, $t2\n")
            storerv(1,res)

        Cgenquad(res,'=',t1+addPlace, termPlace)
        t1 = res
        #########################################
    expressionPlace = res


def boolfactor():
    global tokenID
    global boolfactorTrue
    global boolfactorFalse
    global boolfactorFalseC
    global boolfactorTrueC
    global condFalse
    global condTrue
    global condFalseC
    global condTrueC

    if(tokenID[1]=='nottk'):
        tokenID = lex()
        if(tokenID[1]=='[tk'):
            tokenID = lex()
            condition()
            if(tokenID[1]==']tk'):
                tokenID = lex()
                #######middle code {p1}#######
                boolfactorTrue = condFalse
                boolfactorTrueC = condFalseC
                boolfactorFalse = condTrue
                boolfactorFalseC = condTrueC
	            #####################################
            else:
                print('Syntax error: A "]" was expected in line:', line)
                exit()
        else:
            print('Syntax error: A "["  was expected in line:', line)
            exit()
    elif(tokenID[1]=='[tk'):
        tokenID = lex()
        condition()

        if(tokenID[1]==']tk'):
            tokenID = lex()
            #######middle code {p2}#######
            boolfactorTrue = condTrue
            boolfactorFalse = condFalse
            boolfactorTrueC = condTrueC
            boolfactorFalseC = condFalseC
	        #####################################
        else:
            print('Syntax error: A "]" was expected in line:', line)
            exit()
    elif(tokenID[1]=='+tk' or tokenID[1]=='-tk' or tokenID[1]=='constanttk' or tokenID[1]=='(tk' or tokenID[1]=='idtk'):
        #########middle code {p3}#########
        expression()
        e1 = expressionPlace
        relationalOper()
        relop = relationOperPlace
        expression()
        e2 = expressionPlace
        boolfactorTrue = makelist(nextquad())
        boolfactorTrueC = makelist(clabel+1)
        genquad(relop, e1, e2, '')
        Cgenquad('if (', e1+relop+e2, ') goto ', ' ')
        f3.write("L" + str(labelcounter) + ":\n")
        if(relop=='='):
            loadvr(e1,1)
            loadvr(e2,2)
            f3.write("    beq $t1, $t2, \n")
        elif(relop=='>'):
            loadvr(e1,1)
            loadvr(e2,2)
            f3.write("    bgt $t1, $t2, \n")
        elif(relop=='<'):
            loadvr(e1,1)
            loadvr(e2,2)
            f3.write("    blt $t1, $t2, \n")
        elif(relop=='>='):
            loadvr(e1,1)
            loadvr(e2,2)
            f3.write("    bge $t1, $t2, \n")
        elif(relop=='<='):
            loadvr(e1,1)
            loadvr(e2,2)
            f3.write("    ble $t1, $t2, \n")
        elif(relop=='<>'):
            loadvr(e1,1)
            loadvr(e2,2)
            f3.write("    bne $t1, $t2, \n")
        boolfactorFalse = makelist(nextquad())
        boolfactorFalseC = makelist(clabel+1)
        genquad('jump', '', '', '')
        Cgenquad('goto ', '', '', '')
        ########################################
        f3.write("L" + str(labelcounter) + ":\n")
        f3.write("    j\n")
    else:
        print('Syntax error: The keyword "not" or a "[" or a expression was expected in line:', line)
        exit()


def boolterm():
    global tokenID
    global booltermTrue
    global booltermFalse
    global booltermTrueC
    global booltermFalseC
    global boolfactorFalse
    global boolfactorTrue
    global boolfactorFalseC
    global boolfactorTrueC

    boolfactor()
    #######middle code {p1}#######
    booltermTrue = boolfactorTrue
    booltermTrueC = boolfactorTrueC
    booltermFalse = boolfactorFalse
    booltermFalseC = boolfactorFalseC
    #####################################
    while (tokenID[1]=='andtk'):
        tokenID = lex()
        #######middle code {p2}#######
        backpatch(booltermTrue, nextquad())
        Cbackpatch(booltermTrueC, clabel+1)
        #####################################
        boolfactor()
        #######middle code {p3}#######
        booltermFalse = mergelist(booltermFalse, boolfactorFalse)
        booltermFalseC = mergelist(booltermFalseC, boolfactorFalseC)
        booltermTrue = boolfactorTrue
        #####################################


def condition():
    global tokenID
    global condFalse
    global condTrue
    global condTrueC
    global condFalseC
    global booltermFalse
    global booltermFalseC
    global booltermTrueC
    global booltermTrue
    global clabel

    boolterm()
    #######middle code {p1}#######
    condTrue = booltermTrue
    condFalse = booltermFalse
    condTrueC = booltermTrueC
    condFalseC = booltermFalseC
    #####################################
    while(tokenID[1]=='ortk'):
        tokenID = lex()
        #######middle code {p2}#######
        backpatch(condFalse, nextquad())
        Cbackpatch(condFalseC, clabel+1)
        #####################################
        boolterm()
        #######middle code {p3}#######
        condFalse = booltermFalse
        condFalseC = booltermFalseC
        condTrue = mergelist(condTrue, booltermTrue)
        condTrueC = mergelist(condTrueC, booltermTrueC)
        #####################################

expByPar = False     # if True means that the expression comes from a in parameter
def actualpariterm():
    global tokenID
    global expressionPlace
    global assigmentStatPlace
    global nestingLevel
    global levelOfEntity
    global offsetOfEntity
    global typeOfEntity
    global levelCaller
    global par_counter
    global frCallee
    global expByPar
    par_offset = 12 + 4*par_counter

    f3.write("L" + str(labelcounter+1) + ":\n")
    if(par_counter==0):       # only before the first parameter
        f3.write("    add $fp, $sp, " + str(frCallee) + "\n")
    if(tokenID[1]=='intk'):
        tokenID = lex()
        expByPar = True
        expression()
        ###middle code {p1}###
        genquad('par', expressionPlace, 'CV', '')
        #############################
        searchEntity(expressionPlace)
        loadvr(expressionPlace,0)
        f3.write("    sw $t0, -(" + str(par_offset) + ")($fp)\n")
    elif(tokenID[1]=='inouttk'):
        tokenID = lex()
        if(tokenID[1]=='idtk'):
            searchEntity(tokenID[0])
            var=tokenID[0]
            tokenID = lex()
            ###middle code {p2}###
            genquad('par', var, 'REF', '')
            #############################
            if(levelCaller==levelOfEntity):
                if(typeOfEntity=='var' or typeOfEntity=='in' or typeOfEntity=='temp'):
                    f3.write("    add $t0, $sp, -" + str(offsetOfEntity) + "\n")
                    f3.write("    sw $t0, -(" + str(par_offset) + ")($fp)\n")
                elif(typeOfEntity=='inout'):
                    f3.write("    lw $t0, -" + str(offsetOfEntity) + "($sp)\n")
                    f3.write("    sw $t0, -(" + str(par_offset) + ")($fp)\n")
            elif(levelCaller!=levelOfEntity):
                if(typeOfEntity=='var' or typeOfEntity=='in' or typeOfEntity=='temp'):
                    gnvlcode(var)
                    f3.write("    sw $t0, -(" + str(par_offset) + ")($fp)\n")
                elif(typeOfEntity=='inout'):
                    gnvlcode(var)
                    f3.write("    lw $t0, ($t0)\n")
                    f3.write("    sw $t0, -(" + str(par_offset) + ")($fp)\n")
        else:
            print('Syntax error: A "id" was expected in line:', line)
            exit()
    elif(tokenID[1]=='inandouttk'):
        tokenID = lex()
        if(tokenID[1]=='idtk'):
            searchEntity(tokenID[0])
            var= tokenID[0]
            tokenID = lex()
            ###middle code {p3}###
            genquad('par', var, 'CP(inandou)', '')
            #############################
            loadvr(var,0)
            f3.write("    sw $t0, -(" + str(par_offset) + ")($fp)\n")
            f3.write("    lw $t0, -(" +str(par_offset) + ")($sp)\n")
            storerv(0,var)
        else:
            print('Syntax error: A "id" was expected in line:', line)
            exit()
    elif(tokenID[1]!='intk' and tokenID[1]!='inouttk' and tokenID[1]!='inandouttk'):
        print('Syntax error: One of the keywords "in" "inout" "inandout" was expected in line:', line)
        exit()


par_counter = 0    # here we keep the number of each parameter(fist par, second par...)
def actualparlist():
    global tokenID
    global par_counter
    global assigmentStatPlace

    if(tokenID[1]=='intk' or tokenID[1]=='inouttk' or tokenID[1]=='inandouttk'):
        actualpariterm()
        while(tokenID[1]==',tk'):
            tokenID = lex()
            par_counter += 1
            actualpariterm()


def actualpars():
    global tokenID
    global par_counter

    if(tokenID[1]=='(tk'):
        tokenID = lex()
        par_counter = 0
        actualparlist()
        if(tokenID[1]==')tk'):
            tokenID = lex()
        else:
            print('Syntax error: A ")" was expected in line:', line)
            exit()
    else:
        print('Syntax error: A "(" was expected in line:', line)
        exit()


def inputStat():
    global tokenID

    if(tokenID[1]=='inputtk'):
        tokenID=lex()
        if(tokenID=='idtk'):
            ###middle code###
            genquad('inp', '', '', tokenID[0])
            ########################
            ###assemble code for inputStat####
            f3.write("L" + str(labelcounter) + ":\n")
            f3.write("    li $v0, 5\n")
            f3.write("    syscall\n")
            ###########################
            searchEntity(tokenID[0])
            tokenID=lex()
        else:
            print('Syntax error: A "id" was expected in line:', line)
            exit()
    else:
        print('Syntax error: The keyword "input" was expected in line:', line)
        exit()


def printStat():
    global tokenID
    global expressionPlace

    if(tokenID[1]=='printtk'):
        tokenID = lex()
        expression()
        ###middle code###
        genquad('out', '', '', expressionPlace)
        ########################
        ###assemble code for printStat###
        f3.write("L" + str(labelcounter) + ":\n")
        f3.write("    li $v0, 1\n")
        f3.write("    li, $a0, " + expressionPlace + "\n")
        f3.write("    syscall\n")
        ############################
    else:
        print('Syntax error: The keyword "print" was expected in line:', line)
        exit()


def returnStat():
    global tokenID
    global expressionPlace

    if(tokenID[1]=='returntk'):
        tokenID = lex()
        expression()
        ###middle code###
        genquad('retv', '', '', expressionPlace)
        ########################
        ###assemble code for returnStat###
        f3.write("L" + str(labelcounter) + ":\n")
        loadvr(expressionPlace,1)
        f3.write("    lw $t0, -8($sp)\n")
        f3.write("    sw $t1, ($t0)\n")
        ############################
    else:
        print('Syntax error: The keyword "return" was expected in line:', line)
        exit()


def incaseStat():
    global tokenID
    global clabel
    global condFalse
    global condFalseC
    global condTrue
    global condTrueC

    if(tokenID[1]=='incasetk'):
        tokenID = lex()
        ###middle code {p1}###
        flag = str(nextquad())
        flagC = str(clabel+1)
        state = newTemp()
        genquad(':=', '0', '', state)
        Cgenquad(state, '=', '','0')
        #############################
        newEntity(state, 'temp')
        f3.write("L" + str(labelcounter) + ":\n")
        loadvr('0',1)
        storerv(1,state)
        while(tokenID[1]=='whentk'):
            tokenID = lex()
            if(tokenID[1]=='(tk'):
                tokenID = lex()
                condition()
                ###middle code {p2}###
                backpatch(condTrue, nextquad())
                Cbackpatch(condTrueC, clabel+1)
                #############################
                if(tokenID[1]==')tk'):
                    tokenID = lex()
                    if(tokenID[1]==':tk'):
                        tokenID = lex()
                        statements()
                        ###middle code {p3}###
                        genquad(':=', '1', '', state)
                        Cgenquad(state, '=', '', '1')
                        backpatch(condFalse, nextquad())
                        Cbackpatch(condFalseC, clabel+1)
                        #############################
                        f3.write("L" + str(labelcounter) + ":\n")
                        loadvr('1',1)
                        storerv(1,state)
                    else:
                        print('Syntax error: A ":" was expected in line:', line)
                        exit()
                else:
                    print('Syntax error: A ")" was expected in line:', line)
                    exit()
            else:
                print('Syntax error: A "(" was expected in line:', line)
                exit()
        if(tokenID[1]=='endincasetk'):
            tokenID = lex()
            genquad('=', state, '1', flag)
            Cgenquad('if ','('+state+'== 1)','goto', flagC )
            f3.write("L" + str(labelcounter) + ":\n")
            loadvr(state,1)
            loadvr('1',2)
            f3.write("    beq $t1, $t2, " + str(flag) + "\n")
        else:
            print('Syntax error: The keyword "endincase" was expected in line:', line)
            exit()
    else:
        print('Syntax error: The keyword "incase" was expected in line:', line)
        exit()

exitlist = []
def forcaseStat():
    global tokenID
    global clabel
    global condFalse
    global condFalseC
    global condTrueC
    global exitlist
    global condTrueC

    if(tokenID[1]=='forcasetk'):
        tokenID = lex()
        ###middle code {p1}###
        flagquad = str(nextquad())
        flagquadC= str(clabel+1)
        exitlist = emptylist()
        exitListC= emptylist()
        #############################
        while(tokenID[1]=='whentk'):
            tokenID = lex()
            if(tokenID[1]=='(tk'):
                tokenID = lex()
                condition()
                if(tokenID[1]==')tk'):
                    tokenID = lex()
                else:
                    print('Syntax error: A ")" was expected in line:', line)
                    exit()
            else:
                print('Syntax error: A "(" was expected in line:', line)
                exit()


            if(tokenID[1]==':tk'):
                ###middle code {p2}###
                backpatch(condTrue, nextquad())
                Cbackpatch(condTrueC, clabel+1)
                ############################
                tokenID = lex()
                statements()
                ###middle code {p3}###
                exitlist.append(nextquad())
                exitListC.append(clabel+1)
                genquad('jump', '', '', '')
                Cgenquad ('goto', '', '', '')
                f3.write("L" + str(labelcounter) + ":\n")
                f3.write("    jj\n")
                backpatch(condFalse, nextquad())
                Cbackpatch(condFalseC, clabel+1)
                #############################
            else:
                print('Syntax error: A ":" was expected in line:', line)
                exit()
        if(tokenID[1]=='defaulttk'):
            tokenID = lex()
            if(tokenID[1]==':tk'):
                tokenID =lex()
                statements()
                if(tokenID[1]=='enddefaulttk'):
                    tokenID = lex()
                    ###middle code {p4}###
                    genquad('jump', '', '', flagquad)
                    Cgenquad('goto', '', '', flagquadC)
                    ######################
                    f3.write("L" + str(labelcounter) + ":\n")
                    f3.write("    j L" + flagquad + "\n")
                    if(tokenID[1]=='endforcasetk'):
                        tokenID = lex()
                        ###middle code {p5}###
                        backpatch(exitlist, nextquad())
                        Cbackpatch( exitListC, clabel+1)
                        #############################
                    else:
                        print('Syntax error: The keyword "endforcase" was expected in line:', line)
                        exit()
                else:
                    print('Syntax error: The keyword "enddefault" was expected in line:', line)
                    exit()
            else:
                print('Syntax error: A ":" was expected in line:', line)
                exit()
        else:
            print('Syntax error: The keyword "default" was expected in line:', line)
            exit()

    else:
        print('Syntax error: The keyword "forcase" was expected in line:', line)
        exit()


def exitStat():
    global tokenID
    global exitList
    global existListC
    global numExit
    global clabel

    if(tokenID[1]=='exittk'):
        tokenID = lex()
        ###middle code###
        numExit += 1
        exitList.append(makelist(nextquad()))
        exitListC.append(clabel+1)
        genquad('jump', '', '', '')
        Cgenquad('goto', '', '', '')
        ########################
        f3.write("L" + str(labelcounter) + ":\n")
        f3.write("    k\n")
    else:
        print('SyntaX Error: The keyword "exit" was expected in line:', line)
        exit()


def loopStat():
    global tokenID
    global clabel
    global exitList
    global exitListC
    global numExit

    if(tokenID[1]=='looptk'):
        tokenID = lex()
        ###middle code {p1}###
        flag = str(nextquad())
        flagC= str(clabel+1)
        #############################
        statements()
        ###middle code {p2}###
        genquad('jump', '', '', flag)
        Cgenquad('goto', '', '', flagC)
        #############################
        f3.write("L" + str(labelcounter) + ":\n")
        f3.write("    j L" + flag + "\n")
        if(tokenID[1]=='endlooptk'):
            ###middle code {p3}###
            backpatch(exitList[numExit - 1], nextquad())
            Cbackpatch(exitListC, clabel+1)
            ######################
            numExit -= 1
            tokenID = lex()
        else:
            print('Syntax error: The keyword "endloop" was expected in line:', line)
            exit()
    else:
        print('Syntax error: The keyword "loop" was expected in line:', line)
        exit()


def doWhileStat():
    global tokenID
    global clabel
    global condFalseC
    global condTrueC
    global condTrue
    global condFalse

    if(tokenID[1]=='dowhiletk'):
        tokenID = lex()
        ###middle code {p1}###
        flag = str(nextquad())
        flagC = str(clabel+1)
        #############################
        statements()
        if(tokenID[1]=='enddowhiletk'):
            tokenID = lex()
            if(tokenID[1]=='(tk'):
                tokenID = lex()
                condition()
                ###middle code {p2}###
                backpatch(condTrue, flag)
                backpatch(condFalse, nextquad())
                Cbackpatch(condTrueC, flagC)
                Cbackpatch(condFalseC, clabel+1)
                #############################
                if(tokenID[1]==')tk'):
                    tokenID = lex()
                else:
                    print('Syntax error: A ")" was expected in line:', line)
                    exit()
            else:
                print('Syntax error: A "(" was expected in line:', line)
                exit()
        else:
            print('Syntax error: The keyword "enddowhile" was expected in line:', line)
            exit()
    else:
        print('Syntax error: The keyword "dowhile" was expected in line:', line)
        exit()


def whileStat():
    global tokenID
    global clabel
    global condFalse
    global condFalseC
    global condTrue
    global condTrueC

    if(tokenID[1]=='whiletk'):
        tokenID = lex()
        ###middle code {p1}###
        flag = str(nextquad())
        flagC = str(clabel+1)
        #############################
        if(tokenID[1]=='(tk'):
            tokenID = lex()
            condition()
            if(tokenID[1]==')tk'):
                tokenID = lex()
            else:
                print('Syntax error: A ")" was expected in  line', line)
                exit()
        else:
            print('Syntax error: A "(" was expected in line', line)
            exit()
        ###middle code {p2}###
        backpatch(condTrue, flag)
        Cbackpatch(condTrueC, flagC)
        #############################
        statements()
        if(tokenID[1]=='endwhiletk'):
            tokenID = lex()
            ###middle code {p3}###
            genquad('jump', '', '', flag)
            Cgenquad('goto', '', '', flagC)
            f3.write("L" + str(labelcounter) + ":\n")
            f3.write("    j" + flag + "\n")
            backpatch(condFalse, nextquad())
            Cbackpatch(condFalseC, clabel+1)
            #############################
        else:
            print('Syntax error: The keyword "endwhile" was expected in line:', line)
            exit()
    else:
        print('Syntax error: The keyword "while" was expected in line', line)
        exit()


def elsepart():
    global tokenID

    if(tokenID[1]=='elsetk'):
        tokenID = lex()
        statements()


def ifStat():
    global tokenID
    global condFalse
    global condFalseC
    global condTrue
    global condTrueC


    if(tokenID[1]=='iftk'):   # It isnt necessary
        tokenID = lex()
        if(tokenID[1]=='(tk'):
            tokenID = lex()
            condition()
            if(tokenID[1]==')tk'):
                tokenID = lex()
            else:
                print('Syntax error: A ")" was expected in line:', line)
                exit()
        else:
            print('Syntax error: A "(" was expected in line:', line)
            exit()

        if(tokenID[1]=='thentk'):
            tokenID = lex()
            ###middle code {p1}###
            backpatch(condTrue , nextquad())
            Cbackpatch(condTrueC , clabel+1)
            #############################
            statements()
            ###middle code {p2}###
            iflist = makelist(nextquad())
            iflistc=makelist(clabel+1)
            genquad('jump', '', '', '')
            Cgenquad('goto', '', '', '')
            f3.write("L" + str(labelcounter) + ":\n")
            f3.write("    j\n")
            backpatch(condFalse , nextquad())
            Cbackpatch(condFalseC, clabel + 1)
            #############################

            elsepart()
            ###middle code {p3}###
            backpatch(iflist , nextquad())
            Cbackpatch(iflistc, clabel+1)
            #############################
            if(tokenID[1]=='endiftk'):
                tokenID = lex()
            else:
                print('Syntax error: The keyword "endif" was expected in line:', line)
                exit()
        else:
            print('Syntax error: The keyword "then" was expected in line:', line)
            exit()
    else:
        print('Syntax error: The keyword "if" was expected in line:', line)   # it isnt necessary
        exit()


def assigmentStat():
    global tokenID
    global expressionPlace
    global assigmentStatPlace
    global typeOfEntity
    global offsetOfEntity
    global levelOfEntity

    if(tokenID[1]=='idtk'):
        searchEntity(tokenID[0])
        assigmentStatPlace= tokenID[0]
        tokenID = lex()
        if(tokenID[1]==':=tk'):

            tokenID = lex()
            expression()
            ###middle code###
            genquad(':=', expressionPlace, '', assigmentStatPlace)
            ########################
            ###assemble code for assigment##
            f3.write("L" + str(labelcounter) + ":\n")
            loadvr(expressionPlace,1)
            storerv(1,assigmentStatPlace)
            ########################
            Cgenquad(assigmentStatPlace ,'=','',expressionPlace)
        else:
            print('Syntax error: A ":=" was expected in line:', line)
            exit()
    else:
        print('Syntax error: A "id" was expected in line:', line)
        exit()


def statement():
    global tokenID

    if(tokenID[1]=='idtk'):
        assigmentStat()
    elif(tokenID[1]=='iftk'):
        ifStat()
    elif(tokenID[1]=='whiletk'):
        whileStat()
    elif(tokenID[1]=='dowhiletk'):
        doWhileStat()
    elif(tokenID[1]=='looptk'):
        loopStat()
    elif(tokenID[1]=='exittk'):
        exitStat()
    elif(tokenID[1]=='returntk'):
        returnStat()
    elif(tokenID[1]=='inputtk'):
        inputStat()
    elif(tokenID[1]=='printtk'):
        printStat()
    elif(tokenID[1]=='forcasetk'):
        forcaseStat()
    elif(tokenID[1]=='incasetk'):
        incaseStat()


def statements():
    global tokenID

    statement()
    while(tokenID[1]==';tk'):
        tokenID = lex()
        statement()


def formalparlist():
    global tokenID

    if(tokenID[1]=='intk' or tokenID[1]=='inouttk' or tokenID[1]=='inandouttk'):
        formalparitem()
        while(tokenID[1]==',tk'):
            tokenID = lex()
            formalparitem()


def formalparitem():
    global tokenID
    global nameFunc

    if(tokenID[1]=='intk'):
        tokenID = lex()
        if(tokenID[1]=='idtk'):
            newEntity(tokenID[0], 'in')
            newArgument(nameFunc, 'in')
            tokenID = lex()
        else:
            print('Syntax error: A "id" was expected in line:', line)
            exit()
    elif(tokenID[1]=='inouttk'):
        tokenID = lex()
        if(tokenID[1]=='idtk'):
            newEntity(tokenID[0], 'inout')
            newArgument(nameFunc, 'inout')
            tokenID = lex()
        else:
            print('Syntax error: A "id" was expected in line:', line)
            exit()
    elif(tokenID[1]=='inandouttk'):
        tokenID = lex()
        if(tokenID[1]=='idtk'):
            newEntity(tokenID[0], 'inandout')
            newArgument(nameFunc, 'inandout')
            tokenID = lex()
        else:
            print('Syntax error: A "id" was expected in line:', line)
            exit()
    else:
        print('Syntax error: One of the keywords "in" "inout" "inaandout" was expected in line:', line)
        exit()


def formalpars():
    global tokenID

    if(tokenID[1]=='(tk'):
        tokenID = lex()
        formalparlist()
        if(tokenID[1]==')tk'):
            tokenID = lex()
        else:
            print('Syntax error: A ")" was expected in line:', line)
            exit()
    else:
        print('Syntax error: A "(" was expected in line:', line)
        exit()


def funcbody():
    formalpars()
    block()


def subprogram():
    global tokenID
    global firstquad
    global nameFunc
    nameFunc2 = ''
    global levelOfEntity

    if(tokenID[1]=='functiontk'):
        tokenID = lex()
        if(tokenID[1]=='idtk'):
            nameFunc = tokenID[0]
            nameFunc2 = tokenID[0]
            genquad('begin_block', nameFunc2, ' ', ' ')
            firstquad = labelcounter
            f3.write("L" + str(labelcounter) + ":\n")
            f3.write("    sw $ra, ($sp)\n")
            newEntity(tokenID[0], 'func')
            tokenID = lex()
            funcbody()

            if(tokenID[1]=='endfunctiontk'):
                deleteScope()
                genquad('end_block', nameFunc2, ' ', ' ')
                f3.write("L" + str(labelcounter) + ":\n")
                f3.write("    lw $ra, ($sp)\n")
                f3.write("    jr $ra\n")
                tokenID = lex()
            else:
                print('Syntax error: The keyword "endfunction" was expected in line:', line)
                exit()
        else:
            print('SYntax error: A "id" was expected in line:', line)
            exit()
    else:
        print('Syntax error: The keyword "function" was expected in line:', line)
        exit()


def subprograms():
    global tokenID

    while(tokenID[1]=='functiontk'):
        subprogram()


def varlist():
    global tokenID

    if(tokenID[1]=='idtk'):
        newEntity(tokenID[0], 'var')
        varListC = [tokenID[0]]
        tokenID = lex()
        while(tokenID[1]==',tk'):
            tokenID = lex()
            if(tokenID[1]=='idtk'):
                newEntity(tokenID[0], 'var')
                varListC.append(tokenID[0])
                tokenID = lex()
            else:
                print('Syntax error: A "id" was expected in line:', line)
                exit()
        for i in range(0, len(varListC)):
            Cgenquad('int', ' ', ' ', varListC[i])


def declarations():
    global tokenID

    while(tokenID[1]=='declaretk'):
        tokenID = lex()
        varlist()
        if(tokenID[1]==';tk'):
            tokenID = lex()
        else:
            print('Syntax error: A ";" was expected in line:', line)
            exit()


def block():
    declarations()
    subprograms()
    statements()

frMain = 0       # here we keep the framelength of main
def program() :
    global tokenID
    global quads
    global Cquads
    global scope
    global entity
    global frMain
    global labelList
    global loopLabels
    global ifList
    namemain = ''
    tokenID = lex()   #first time

    if(tokenID[1]=='programtk'):
        tokenID = lex()
        if(tokenID[1]=='idtk'):
            namemain = tokenID[0]
            genquad('begin_block', tokenID[0], ' ', ' ')
            f3.write("Lmain:\n")
            f3.write("    add $sp, $sp, " + str(frMain) + "\n")
            f3.write("    move $s0, $sp\n")
            tokenID = lex()
            block()
        else:
            print('Syntax error: A "id" must be added after the keyword program')
            exit()
        if(tokenID[1]=='endprogramtk'):
            tokenID = lex()
            genquad('halt', ' ', ' ', ' ')
            f3.write("L" + str(labelcounter) + ":\n")
            f3.write("    li, v0, 10\n")
            f3.write("    syscall\n")
            genquad('end_block', namemain, ' ', ' ')
            f3.write("L" + str(labelcounter) + ":\n")
            if(tokenID[1]!='EOFtk'):
                print('Syntax error: A starlet program must finist with "endprogram" as keyword')
                exit()
            else:
                print('The starlet programm was compiled without problem')
                if not scope:
                    max = entity[0][2]
                    for i in range(1,len(entity)):
                        if(entity[i][2]>max):
                            max = entity[i][2]
                    frMain = max + 4
                else:
                    max = 0
                    for k in range(0, len(scope)):
                        for p in range(0, len(scope[k][0])):
                            if(scope[k][0][p][0]=='var' or scope[k][0][p][0]=='temp'):
                                if max<scope[k][0][p][2]:
                                    max = scope[k][0][p][2]
                    for i in range(0,len(entity)):
                        if(entity[i][2]>max):
                            max = entity[i][2]
                    frMain = max + 4
                for i in range(0, len(quads)):
                    for j in range(0, len(quads[i])):
                        f1.write(quads[i][j]+' ')
                    f1.write('\n')
                f2.write('int main { \n')
                for i in range(0, len(Cquads)):
                    for j in range(0, len(Cquads[i])):
                        f2.write(Cquads[i][j]+' ')
                    f2.write('\n')
                f2.write('}')
                f3.seek(0)
                i = 0
                j = 0
                k = len(ifList)-1
                
                while True:         # we copy f3 into f4 adding the labels, which we have kept in labelList
                    nextline = f3.readline()
                    if(nextline=="    k\n"):
                        f4.write("    j L" + str(ifList[k]) + "\n")
                        k-=1
                    elif(nextline=="    jj\n"):
                        f4.write("    j L" + str(loopLabels[j]) + "\n")
                        j+=1
                    elif(nextline=="    j\n"):
                        f4.write("    j L" + str(labelList[i]) + "\n")
                        i+=1
                    elif(nextline=="    beq $t1, $t2, \n"):
                        f4.write("    beq $t1, $t2, L" + str(labelList[i]) + "\n")
                        i+=1
                    elif(nextline=="    bgt $t1, $t2, \n"):
                        f4.write("    bgt $t1, $t2, L" + str(labelList[i]) + "\n")
                        i+=1
                    elif(nextline=="    blt $t1, $t2, \n"):
                        f4.write("    blt $t1, $t2, L" + str(labelList[i]) + "\n")
                        i+=1
                    elif(nextline=="    ble $t1, $t2, \n"):
                        f4.write("    ble $t1, $t2, L" + str(labelList[i]) + "\n")
                        i+=1
                    elif(nextline=="    bge $t1, $t2, \n"):
                        f4.write("    bge $t1, $t2, L" + str(labelList[i]) + "\n")
                        i+=1
                    elif(nextline=="    bne $t1, $t2, \n"):
                        f4.write("    bne $t1, $t2, L" + str(labelList[i]) + "\n")
                        i+=1
                    elif not nextline:
                        break
                    else:
                        f4.write(nextline)
                os.remove("test.asm")        # now we delete f3 file
                exit()
        else:
            print('Syntax error: "endprogram" was expected in line:', line)
            exit()
    else:
        print('Syntax error: A starlet program must start with "program" as keyword')
        exit()


def newScope():
    global scope
    global entity
    global nestingLevel
    global offset

    scope = [[entity, nestingLevel]] + scope
    offset = 12
    entity = []
    nestingLevel += 1


def deleteScope():
    global scope
    global nestingLevel
    global entity
    global entertoScopeNow
    global offset

    if not entity:
        for i in range(0, len(scope)-1):
            if(scope[i][1]==nestingLevel):
                del(scope[i])
        nestingLevel -= 1
        for i in range(0, len(scope)):
            if(scope[i][1]==nestingLevel):
                max = scope[i][0][0][2]
                for j in range(1, len(scope[i][0])):
                    if(scope[i][0][j][2]>max):
                        max = scope[i][0][j][2]
                offset = max + 4
        entertoScopeNow = False
    else:
        for i in range(0, len(scope)-1):
            if(scope[i][1]==nestingLevel):
                del(scope[i])
        del(entity)
        entertoScopeNow = True
        nestingLevel -= 1
        for i in range(0, len(scope)):
            if(scope[i][1]==nestingLevel):
                max = scope[i][0][0][2]
                for j in range(1, len(scope[i][0])):
                    if(scope[i][0][j][2]>max):
                        max = scope[i][0][j][2]
                offset = max + 4
        entity = []
    for i in range(0, len(scope)):
        if(scope[i][1]==nestingLevel):
            for j in range(0, len(scope[i][0])):
                if(scope[i][0][j][0]=='func'):
                    scope[i][0][j][4] = offset             # we update the framelength


def newEntity(name, type):
    global offset
    global entity
    global firstquad
    global nestingLevel
    global entertoScopeNow
    global scope

    if(type=='var'):
        entity = [['var', name, offset]] + entity
        offset += 4
    elif(type=='func'):
        entity = [['func', name, firstquad, [], 0]] + entity
        newScope()
    elif(type=='temp'):
        entity = [['temp', name, offset]] + entity
        offset += 4
    elif(type=='in'):
        entity = [['in', name, offset]] + entity
        offset += 4
    elif(type=='inout'):
        entity = [['inout', name, offset]] + entity
        offset += 4
    else:
        entity = [['inandout', name, offset]] + entity
        offset += 4

    if(entertoScopeNow==True):
        for i in range(0, len(scope)-1):
            if(scope[i][1]==nestingLevel):
                scope[i][0].append(entity[0])
                entity = []


def newArgument(nameFunc, paritem):
    global scope
    global nestingLevel

    if(paritem=='in'):
        for i in range(0, len(scope)):
            for j in range(0, len(scope[i][0])):
                if(scope[i][0][j][0]=='func' and scope[i][1]==nestingLevel-1 and scope[i][0][j][1]==nameFunc):
                    scope[i][0][j][3].append('in')
    elif(paritem=='inout'):
        for i in range(0, len(scope)):
            for j in range(0, len(scope[i][0])):
                if(scope[i][0][j][0]=='func' and scope[i][1]==nestingLevel-1 and scope[i][0][j][1]==nameFunc):
                    scope[i][0][j][3].append('inout')
    else:
        for i in range(0, len(scope)):
            for j in range(0, len(scope[i][0])):
                if(scope[i][0][j][0]=='func' and scope[i][1]==nestingLevel-1 and scope[i][0][j][1]==nameFunc):
                    scope[i][0][j][3].append('inandout')


levelOfEntity = 0
offsetOfEntity = 0
typeOfEntity = ''
found = False
exist = False

# @searchEntity(): for every variable in our stl program checks
# ---------------- if it exists in symbol matrix and determines
# ---------------- its levelscope as well as its offset and type
def searchEntity(name):
    global entity
    global scope
    global nestingLevel
    global found
    global exist
    global levelOfEntity
    global offsetOfEntity
    global typeOfEntity

    if not entity:
        for j in range(0,len(scope)):
            for k in range(0,len(scope[j][0])):
                if(scope[j][0][k][1]==name):
                    levelOfEntity = scope[j][1]
                    offsetOfEntity = scope[j][0][k][2]
                    typeOfEntity = scope[j][0][k][0]
                    found = True
                    exist = True
                    break
            if(found == True):
                break;
    else:
        for i in range(0, len(entity)):
            if(entity[i][1]==name):
                exist = True
                levelOfEntity = nestingLevel
                offsetOfEntity = entity[i][2]
                typeOfEntity = entity[i][0]
                found = True
                break
        if(found == False):
            for j in range(0,len(scope)):
                for k in range(0,len(scope[j][0])):
                    if(scope[j][0][k][1]==name):
                        levelOfEntity = scope[j][1]
                        offsetOfEntity = scope[j][0][k][2]
                        typeOfEntity = scope[j][0][k][0]
                        found = True
                        exist = True
                        break
                if(found == True):
                    break;
    found = False

    if(exist==False and not(name.isdigit()) and name!='main'):
        print("the " + name + " in line " + str(line) + " is not declared")
        exit()
    exist = False


frCallee = 0     # here we keep the framelength of function called
fqCallee = 0     # here we keep the firstquad of function called
caller = ''      # here we keep the name of function, which call the called function
found = False
lvlcaller = 0    # the nestingLevel of caller function
# @frCalleeAndFindCalller: determine the framelength of callee function
# -----------------------  and find the function which called her (caller)
def frCalleeAndFindCalller(funcname):
    global frCallee
    global caller
    global found
    global scope
    global lvlcaller
    global fqCallee

	# find the framelength of callee function
    for i in range(0, len(scope)):
        for j in range(0, len(scope[i][0])):
            if(scope[i][0][j][1]==funcname):
                frCallee = scope[i][0][j][4]
                fqCallee = scope[i][0][j][2]
                if(scope[i][1]>1):
                    lvlcaller = scope[i][1] - 1
                else:
                    lvlcaller = scope[i][1]
                found = True
                break
        if(found==True):
            break
    found = False
    # find the caller function
    for i in range(0,len(scope)):
        for j in range(0,len(scope[i][0])):
            if(scope[i][1]==lvlcaller and scope[i][0][j][0]=='func' and scope[i][0][j][4]==0):
                caller = scope[i][0][j][1]
                found = True
                break
        if(found==True):
            break
    if(found==False):
        caller = 'main'

    found = False
    lvlcaller = 0


# @gnvlcode(): transfer the address of a non-local variable
# -----------  in $t0 register
def gnvlcode(var):
    global nestingLevel
    global levelOfEntity
    global offsetOfEntity

    searchEntity(var)
    upperLevel = levelOfEntity
    f3.write("    lw  $t0, -4($sp)\n")
    upperLevel += 1
    while(nestingLevel>upperLevel):
        f3.write("    lw $t0, -4($t0)\n")
        upperLevel += 1
    f3.write("    add $t0, $t0, -" + str(offsetOfEntity) + "\n")


# @loadvr(): transfer data in $tr register
def loadvr(v,r):
    global nestingLevel
    global levelOfEntity
    global offsetOfEntity
    global typeOfEntity

    searchEntity(v)
    if(v.isdigit()):
        f3.write("    li $t" + str(r) + ", " + str(v) + "\n")
    elif(levelOfEntity==1):
        f3.write("    lw $t" + str(r) + ", -" + str(offsetOfEntity) + "($s0)\n")
    elif((levelOfEntity==nestingLevel and (typeOfEntity=="in" or typeOfEntity=="inandout" or typeOfEntity=="var")) or typeOfEntity=="temp"):
        f3.write("    lw $t" + str(r) + ", -" + str(offsetOfEntity) + "($sp)\n")
    elif(typeOfEntity=="inout" and levelOfEntity==nestingLevel):
        f3.write("    lw $t0, -" + str(offsetOfEntity) + "($sp)\n")
        f3.write("    lw $t" + str(r) + ", ($t0)\n")
    elif(levelOfEntity<nestingLevel and (typeOfEntity=="in" or typeOfEntity=="inandout" or typeOfEntity=="var")):
        gnvlcode(v)
        f3.write("    lw $t" + str(r) + ", ($t0)\n")
    elif(typeOfEntity=="inout" and levelOfEntity<nestingLevel):
        gnvlcode(v)
        f3.write("    lw $t0, ($t0)\n")
        f3.write("    lw $t" + str(r) + ", ($t0)\n")


# @storerv(): transfer data from $tr register to memory(variable v)
def storerv(r,v):
    global nestingLevel
    global levelOfEntity
    global offsetOfEntity
    global typeOfEntity

    searchEntity(v)
    if(levelOfEntity==1):
        f3.write("    sw $t" + str(r) + ", -" + str(offsetOfEntity) + "($s0)\n")
    elif((levelOfEntity==nestingLevel and (typeOfEntity=="in"  or typeOfEntity=="inandout" or typeOfEntity=="var")) or typeOfEntity=="temp"):
        f3.write("    sw $t" + str(r) + ", -" + str(offsetOfEntity) + "($sp)\n")
    elif(typeOfEntity=="inout" and levelOfEntity==nestingLevel):
        f3.write("    lw $t0, -" + str(offsetOfEntity) + "($sp)\n")
        f3.write("    sw $t" + str(r) + ", ($t0)\n")
    elif(levelOfEntity<nestingLevel and (typeOfEntity=="in" or typeOfEntity=="inandout" or typeOfEntity=="var")):
        gnvlcode(v)
        f3.write("    sw $t" + str(r) + ", ($t0)\n")
    elif(typeOfEntity=="inout" and levelOfEntity<nestingLevel):
        gnvlcode(v)
        f3.write("    lw $t0, ($t0)\n")
        f3.write("    sw $t" + str(r) + ", ($t0)\n")

program()
