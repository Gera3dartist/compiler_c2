from contextlib import contextmanager
from operator import pos
from  .lexer import tableToPrint, tableOfSymb, tableOfLabel, sourceCode, FSuccess, tableOfId, tableOfConst
from .stack import Stack


# Список для зберігання ПОЛІЗу - 
# коду у постфіксній формі
postfixCode = []
nextInstr = 0
commandTrack = []
stack = Stack()

# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow=1    

# довжина таблиці символів програми 
# він же - номер останнього запису
len_tableOfSymb = 0


toView = False

def postfixTranslator(tableOfSymb):
    global len_tableOfSymb, FSuccess
    len_tableOfSymb = len(tableOfSymb)
    # чи був успішним лексичний розбір
    if (True,'Lexer') == FSuccess:
        FSuccess = parseProgram()
        serv()
        return FSuccess

# Функція для розбору за правилом
# Program = program StatementList end
# читає таблицю розбору tableOfSymb
def parseProgram():
    # global FSuccess
    try:
        # # перевірити наявність ключового слова 'program'
        # parseToken('program','keyword','')  # Трансляція не потрібна
        #                                     # лексема не має операційної семантики 

        # перевірити синтаксичну коректність списку інструкцій StatementList
        parseStatementList()                # Трансляція (тут нічого не робити)  
                                            # ця функція сама згенерує 
                                            # та додасть ПОЛІЗ інструкцій (виразів)

        # повідомити про успішність
        # синтаксичного аналізу 
        # та трансляції програми ПОЛІЗ
        print('Translator: Переклад у ПОЛІЗ та синтаксичний аналіз завершились успішно')
        FSuccess = (True,'Translator')
        return FSuccess
    except SystemExit as e:
        # Повідомити про виняток
        # Тут всі можливі помилки - синтаксичні
        print('Parser: Аварійне завершення програми з кодом {0}'.format(e))

            
# Функція перевіряє, чи у поточному рядку таблиці розбору
# зустрілась вказана лексема lexeme з токеном token
# параметр indent - відступ при виведенні у консоль
def parseToken(lexeme,token,indent):
    # доступ до поточного рядка таблиці розбору
    global numRow
    
    # якщо всі записи таблиці розбору прочитані,
    # а парсер ще не знайшов якусь лексему
    if numRow > len_tableOfSymb :
        failParse('неочікуваний кінець програми',(lexeme,token,numRow))
        
    # прочитати з таблиці розбору 
    # номер рядка програми, лексему та її токен
    numLine, lex, tok = getSymb() 
        
    # тепер поточним буде наступний рядок таблиці розбору
    increment_row()
        
    # чи збігаються лексема та токен таблиці розбору з заданими 
    if (lex, tok) == (lexeme,token):
        return True
    else:
        # згенерувати помилку та інформацію про те, що 
        # лексема та токен таблиці розбору (lex,tok) відрізняються від
        # очікуваних (lexeme,token)
        failParse('невідповідність токенів',(numLine,lex,tok,lexeme,token))
        return False


# Прочитати з таблиці розбору поточний запис
# Повертає номер рядка програми, лексему та її токен
def getSymb():
    if numRow > len_tableOfSymb :
            failParse('getSymb(): неочікуваний кінець програми',numRow)
    # таблиця розбору реалізована у формі словника (dictionary)
    # tableOfSymb[numRow]={numRow: (numLine, lexeme, token, indexOfVarOrConst)
    numLine, lexeme, token, _ = tableOfSymb[numRow]	
    return numLine, lexeme, token        


# Обробити помилки
# вивести поточну інформацію та діагностичне повідомлення 
def failParse(str,tuple):
    if str == 'неочікуваний кінець програми':
        (lexeme,token,numRow)=tuple
        print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format((lexeme,token),numRow))
        exit(1001)
    if str == 'getSymb(): неочікуваний кінець програми':
        numRow=tuple
        print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(numRow,tableOfSymb[numRow-1]))
        exit(1002)
    elif str == 'невідповідність токенів':
        (numLine,lexeme,token,lex,tok)=tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - ({3},{4}).'.format(numLine,lexeme,token,lex,tok))
        exit(1)
    elif str == 'невідповідність інструкцій':
        (numLine,lex,tok,expected)=tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,lex,tok,expected))
        exit(2)
    elif str == 'невідповідність у Expression.Factor':
        (numLine,lex,tok,expected)=tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,lex,tok,expected))
        exit(3)


          
# Функція для розбору за правилом для StatementList 
# StatementList = Statement  { Statement }
# викликає функцію parseStatement() доти,
# доки parseStatement() повертає True
def parseStatementList(block=False):
    # print('\t parseStatementList():')
    while parseStatement(block):
            pass
    return True


def parseStatement(block):
    # прочитаємо поточну лексему в таблиці розбору
    if numRow > len_tableOfSymb:
        return False
    numLine, lex, tok = getSymb()
    # якщо токен - ідентифікатор
    # обробити інструкцію присвоювання
    if tok == 'ident':
        parseAssign()       
        return True

    # якщо лексема - ключове слово 'if'
    # обробити інструкцію розгалуження
    elif (lex, tok) == ('if','keyword'):
        parseIf()
        return True 
    elif (lex, tok) == ('do','keyword'):
        return parse_do_while() 
    elif (lex, tok) == ('}','curbr_op') and block:
        return False

    # тут - ознака того, що всі інструкції були коректно 
    # розібрані і була знайдена остання лексема програми.
    # тому parseStatement() має завершити роботу


    else: 
        # жодна з інструкцій не відповідає 
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій',(numLine,lex,tok,'ident або if'))
        return False

def parseAssign():
    # номер запису таблиці розбору
    global numRow, postfixCode
    # print('\t'*4+'parseAssign():')

    # взяти поточну лексему
    # вже відомо, що це - ідентифікатор
    _numLine, lex, tok = getSymb()

    # починаємо трансляцію інструкції присвоювання за означенням:
    postfixCode.append((lex,tok)) # Трансляція   
                                  # ПОЛІЗ ідентифікатора - ідентифікатор

    if toView: configToPrint(lex,numRow)

    # встановити номер нової поточної лексеми
    increment_row()

    # print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    # якщо була прочитана лексема - '='
    if parseToken('=','assign_op','\t\t\t\t\t'):
        # розібрати арифметичний вираз
        parseExpression()       # Трансляція (тут нічого не робити)  
                                # ця функція сама згенерує 
                                # та додасть ПОЛІЗ виразу       

        postfixCode.append(('=','assign_op'))# Трансляція   
                                # Бінарний оператор  '='
                                # додається після своїх операндів
        if toView: configToPrint('=',numRow)
        return True
    else: return False    

# розбір інструкції розгалуження за правилом
# IfStatement = if BoolExpr then Statement else Statement endif
# функція названа parseIf() замість parseIfStatement()
def parseIf():
    global numRow
    _, lex, tok = getSymb()
    if lex=='if' and tok=='keyword':
        # 'if' нічого не додає до ПОЛІЗу    # Трансляція 
        increment_row()
        parseBoolExpr()  # Трансляція
        with parse_code_block():
            # Згенерувати мітку m1 = (lex,'label')
            m1 = createLabel()
            postfixCode.append(m1)  # Трансляція    
            postfixCode.append(('JF','jf'))   # додали m1 JF   
            parseStatementList(block=True);

        parseToken('else','keyword','\t'*7)
        m2 = createLabel()      
        with parse_code_block():
            # Згенерувати мітку m2 = (lex,'label')
            postfixCode.append(m2)  # Трансляція 1
            postfixCode.append(('JMP','jump'))   # додали m2 JMP m1 : 2
            setValLabel(m1) # в табл. міток {m1: 2}
            postfixCode.append(m1)
            postfixCode.append((':','colon'))
            parseStatementList(block=True);
        setValLabel(m2) # в табл. міток
        postfixCode.append(m2)  # Трансляція
        postfixCode.append((':','colon'))
                
        return True
    else: return False


def createLabel():
    """
    якщо мітки не існує в tableOfLabel  - створити мітку з невизначеним значеннням
    """
    global tableOfLabel
    nmb = len(tableOfLabel)+1
    lexeme = "m"+str(nmb)
    val = tableOfLabel.get(lexeme)
    if val is None:
        tableOfLabel[lexeme] = 'val_undef'
        tok = 'label' # # #
    else:
        tok = 'Конфлікт міток'
        print(tok)
        exit(1003)
    return (lexeme,tok)
    

def setValLabel(lbl):
    """
    для мітки встановити значенням індекс рівний довжині postfixCode
    """
    global tableOfLabel
    lex,_tok = lbl
    tableOfLabel[lex] = len(postfixCode)
    return True


# розбір логічного виразу за правиллом
# BoolExpr = true 
#           | false 
#           | Expression ('='|'<='|'>='|'<'|'>'|'<>') Expression
def parseBoolExpr():
    global numRow
    numLine, lex, tok = getSymb()
    if lex == 'true' or lex == 'false':
        increment_row()
        postfixCode.append((lex,tok))   # Трансляція
        return True
    else:
        parseExpression()
        if numRow > len_tableOfSymb:
            return True    # Трансляція
        numLine, lex, tok = getSymb()
        if (lex, tok) == ('{', 'curbr_op'):
            return True
        
    if tok in ('rel_op'):
        postfixCode.append((lex,tok))   # Трансляція
        # print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    else:
        failParse('mismatch in BoolExpr',(numLine,lex,tok,'relop'))
    return True    


# виводить у консоль інформацію про 
# перебіг трансляції
def configToPrint(lex,numRow):
    stage = '\nКрок трансляції\n'
    stage += 'лексема: \'{0}\'\n'
    stage += 'tableOfSymb[{1}] = {2}\n'
    stage += 'postfixCode = {3}\n'
    # tpl = (lex,numRow,str(tableOfSymb[numRow]),str(postfixCode))
    print(stage.format(lex,numRow,str(tableOfSymb[numRow]),str(postfixCode)))


def parseExpression():
    global numRow, postfixCode
    # print('\t'*5+'parseExpression():')
    _numLine, lex, tok = getSymb()
    parseTerm()                 # Трансляція (тут нічого не робити)    
                                # ця функція сама згенерує 
                                # та додасть ПОЛІЗ доданка
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        if numRow > len_tableOfSymb:
            break
        _numLine, lex, tok = getSymb()
        if tok in ('add_op', 'rel_op'):
            increment_row()
            # print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
            parseTerm()         # Трансляція (тут нічого не робити)    
                                # ця функція сама згенерує 
                                # та додасть ПОЛІЗ доданка
                                
                                # Трансляція 
            postfixCode.append((lex,tok))   
                                # lex - бінарний оператор  '+' чи '-'
                                # додається після своїх операндів
            if toView: configToPrint(lex,numRow)
        else:
            F = False
    return True


def increment_row():
    global numRow
    numRow+=1
    return True


def parseTerm():
    global numRow, postfixCode
    # print('\t'*6+'parseTerm():')
    parseFactor()               # Трансляція (тут нічого не робити)
                                # ця функція сама згенерує 
                                # та додасть ПОЛІЗ множника
    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*' або '/'
    while F:
        if numRow > len_tableOfSymb:
            break
        _numLine, lex, tok = getSymb()

        if tok in ('mult_op') and increment_row():
        
            if lex == '^':
                times = 1
                while (lex == '^'):
                    parseFactor() # this may icrement numRow
                    if numRow > len_tableOfSymb:
                        break
                    _, lex, tok = getSymb()
                    if lex == '^':
                        times +=1
                        increment_row()
                    else:
                        break

                postfixCode.extend([('^','mult_op')]*times)
            else:
                parseFactor()       # Трансляція (тут нічого не робити)    
                                    # ця функція сама згенерує та додасть ПОЛІЗ множника

                                    # Трансляція   
                postfixCode.append((lex,tok))  
                                    # lex - бінарний оператор  '*' чи '/'
                                    # додається після своїх операндів
        else:
            F = False
    return True


def parseFactor():
    global numRow, postfixCode
    # print('\t'*7+'parseFactor():')
    numLine, lex, tok = getSymb()
    # print('\t'*7+'parseFactor()=============рядок: {0}\t (lex, tok):{1}'.format(numLine,(lex, tok)))
    
    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    if tok in ('int','float','ident'):
        postfixCode.append((lex,tok))      # Трансляція
                                # ПОЛІЗ константи або ідентифікатора 
                                # відповідна константа або ідентифікатор

        increment_row()
        # print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    
    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex=='(':
        increment_row()
        parseExpression()       # Трансляція (тут нічого не робити)    
                                # ця функція сама згенерує та додасть ПОЛІЗ множника
                                # дужки у ПОЛІЗ НЕ додаємо
        parseToken(')','par_op','\t'*7)
        # print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    else:
        failParse('невідповідність у Expression.Factor',(numLine,lex,tok,'rel_op, int, float, ident або \'(\' Expression \')\''))
    return True


@contextmanager
def parse_code_block() -> bool:
    """
    розбір конструкції код блок
    CodeBlock = "{", {Newline}  StatementList, {Newline}, "}";
    """
    parseToken('{','curbr_op','\t'*7)
    yield
    parseToken('}','curbr_op','\t'*7)


def parse_do_while() -> bool:
    """
    розбір інструкції do while
    doWhileStatement = "do", CodeBlock, "while", BoolExpr;
    """

    parseToken('do','keyword','\t'*7)
    m1 = createLabel()
    with parse_code_block():
        # set label
        setValLabel(m1) # в табл. міток
        parseStatementList(block=True)
    parseToken('while','keyword','\t'*7)
    parseBoolExpr()

    postfixCode.append(m1)  # add label
    postfixCode.append(('JT','jt'))   # додали m1 JT
    postfixCode.append(m1)
    postfixCode.append((':','colon'))
    return True


def serv():

    # tableToPrint('All')
    # tableToPrint('Label')
    # tableToPrint('Id')
    print('\nПочатковий код програми: \n{0}'.format(sourceCode))
    print('\nКод програми у постфіксній формі (ПОЛІЗ): \n{0}'.format(postfixCode)) 
    for lbl in tableOfLabel:
        print('postfixCode[{0}:{1}]={2}'.format(lbl,tableOfLabel[lbl],postfixCode[tableOfLabel[lbl]]))
    
    return True



def doIt(lex,tok):
    global stack, postfixCode, tableOfId, tableOfConst, tableOfLabel
    if (lex,tok) == ('=', 'assign_op'):
        # зняти з вершини стека запис (правий операнд = число)
        (lexR,tokR) = stack.pop()
        # зняти з вершини стека iдентифiкатор (лiвий операнд)
        (lexL,tokL) = stack.pop()

        # виконати операцiю:
        # оновлюємо запис у таблицi iдентифiкаторiв
        # iдентифiкатор/змiнна
        # (index не змiнюється,
        # тип - як у константи,
        # значення - як у константи)
        tableOfId[lexL] = (tableOfId[lexL][0], tableOfConst[lexR][1], tableOfConst[lexR][2])
        return True
    elif tok in ('add_op','mult_op', 'rel_op'):
        # зняти з вершини стека запис (правий операнд)
        (lexR,tokR) = stack.pop()
        # зняти з вершини стека запис (лiвий операнд)
        (lexL,tokL) = stack.pop()

    if (tokL,tokR) in (('int','float'),('float','int')):
        failRunTime('невiдповiднiсть типiв',((lexL,tokL),lex,(lexR,tokR)))
    elif tok in ('add_op','mult_op', 'rel_op'):
        processing_add_mult_rel_op((lexL,tokL),lex,(lexR,tokR))
        # stack.push()

    return True

def processing_add_mult_rel_op(ltL,lex,ltR):
    global stack, postfixCode, tableOfId, tableOfConst, tableOfLabel
    lexL,tokL = ltL
    lexR,tokR = ltR
    if tokL == 'ident':
        if tableOfId[lexL][1] == 'type_undef':
            failRunTime('неiнiцiалiзована змiнна',
                (lexL,tableOfId[lexL],(lexL,tokL),lex,(lexR,tokR)))

        else:
            valL,tokL = (tableOfId[lexL][2],tableOfId[lexL][1])
    else:
        valL = tableOfConst[lexL][2]
    if tokR == 'ident':
        if tableOfId[lexR][1] == 'type_undef':
            failRunTime('неiнiцiалiзована змiнна',
                (lexR,tableOfId[lexR],(lexL,tokL),lex,(lexR,tokR)))
        else:
            valR,tokR = (tableOfId[lexR][2],tableOfId[lexR][1])
    else:
        valR = tableOfConst[lexR][2]
    getValue((valL,lexL,tokL),lex,(valR,lexR,tokR))



def getValue(vtL,lex,vtR):
    global stack, postfixCode, tableOfId, tableOfConst, tableOfLabel
    valL,lexL,tokL = vtL
    valR,lexR,tokR = vtR
    if (tokL,tokR) in (('int','float'),('float','int')):
        failRunTime('невiдповiднiсть типiв',((lexL,tokL),lex,(lexR,tokR)))
    elif lex == '+':
        value = valL + valR
    elif lex == '-':
        value = valL - valR
    elif lex == '*':
        value = valL * valR
    elif lex == '/' and valR ==0:
        failRunTime('дiлення на нуль',((lexL,tokL),lex,(lexR,tokR)))
    elif lex == '/' and tokL=='float':
        value = valL / valR
    elif lex == '/' and tokL=='int':
        value = int(valL / valR)

    elif lex == '^' and tokL=='int':
        value = float(valL ** valR)
    elif lex == '>':
        value = valL > valR
    elif lex == '<':
        value = valL < valR
    elif lex == '==':
        value = valL == valR
    else:
        failRunTime('не реалізованна поведінка', ((lexL,tokL),lex,(lexR,tokR)))
        raise RuntimeError('NOT IMPLEMENTED')
    stack.push((str(value),tokL))
    toTableOfConst(value,tokL)

def toTableOfConst(value,  token: str):
    tableOfConst[str(value)]=(len(tableOfConst) + 1 ,token, value)


def failRunTime(str,tuple):
    if str == 'невiдповiднiсть типiв':
        ((lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Типи операндiв вiдрiзняються у {0} {1} {2}'.format((lexL,tokL),lex,(lexR,tokR)))
        exit(1)
    elif str == 'неiнiцiалiзована змiнна':
        (lx,rec,(lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Значення змiнної {0}:{1} не визначене. Зустрiлось у {2} {3} {4}'.format(lx,rec,(lexL,tokL),lex,(lexR,tokR)))
        exit(2)
    elif str == 'дiлення на нуль':
        ((lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Дiлення на нуль у {0} {1} {2}. '.format((lexL,tokL),lex,(lexR,tokR)))
        exit(3)


def doJumps(tok, nextInstr):
    global stack
    if tok =='jump':
        _next = processing_JUMP(nextInstr)
    elif tok == 'colon':
        (_, _) = stack.pop()
        _next =  nextInstr + 1
    elif tok =='jf':
        _next = processing_JF(nextInstr)
    elif tok == 'jt':
        _next = processing_JT(nextInstr)
    return _next

def processing_JUMP():
    """
    Функцiя processing_JUMP() знiмає з вершини стека мiтку та повертає зна-
    чення цiєї мiтки як номер iнструкцiї для виконання на наступному кроцi.
    """
    global stack
    (label_name, _) = stack.pop()
    return tableOfLabel[label_name]


def processing_colon():
    """
    Функцiя processing_colon() просто знiмає з вершини стека непотрiбну мiтку
    та встановлює номер iнструкцiї для наступного кроку на одиницю бiльшим за
    поточний номер.
    """
    global stack
    (_, _) = stack.pop()
    return nextInstr + 1

def processing_JF(nextInstr):
    """
    Функцiя processing_JF() знiмає з вершини стека мiтку, потiм знiмає значен-
    ня BoolExpr i, якщо це false – повертає значення мiтки як номер iнструкцiї
    для виконання на наступному кроцi, iнакше – номер, на одиницю бiльшим за
    поточний.
    """
    global stack
    (label_name, _) = stack.pop() # name of label
    (if_value, _) = stack.pop() # value of bool expression
    if if_value.lower() == 'true':
        return nextInstr + 1
    else:
        return tableOfLabel[label_name]


def processing_JT(nextInstr):
    """
    Функцiя processing_JT() знiмає з вершини стека мiтку, потiм знiмає значен-
    ня BoolExpr i, якщо це true – повертає значення мiтки як номер iнструкцiї
    для виконання на наступному кроцi, iнакше – номер, на одиницю бiльшим з     
    поточний.
    """
    global stack
    (label_name, _) = stack.pop() # name of label
    (if_value, _) = stack.pop() # value of bool expression
    if if_value.lower() == 'true':
        return tableOfLabel[label_name]
    else:
        return nextInstr + 1
   

def postfixInterpreter(table_of_symbols):
    FSuccess = postfixTranslator(table_of_symbols)
    # чи була успiшною трансляцiя
    if (True,'Translator') == FSuccess:
        print('\nПостфiксний код: \n{0}'.format(postfixCode))
        return postfixProcessing()
    else:
        # Повiдомити про факт виявлення помилки
        print('Interpreter: Translator завершив роботу аварiйно')
        return False


def postfixProcessing():
    global stack, postfixCode, nextInstr, commandTrack
    cyclesNumb = 0
    maxNumb = len(postfixCode)
    try:
        while (nextInstr < maxNumb and cyclesNumb < 1000):
            cyclesNumb += 1
            lex,tok = postfixCode[nextInstr]
            commandTrack.append((nextInstr,lex,tok))
            if tok in ('int','float','ident','label','bool'):
                stack.push((lex,tok))
                nextInstr+=1
            elif tok in ('jump','jf','colon', 'jt'):
                nextInstr = doJumps(tok, nextInstr)
            else:
                doIt(lex,tok)
                nextInstr+=1
            print('Загальна кiлькiсть крокiв: {0}'.format(cyclesNumb))
    except SystemExit as e:
        # Повiдомити про факт виявлення помилки
        print('RunTime: Аварiйне завершення програми з кодом {0}'.format(e))
    finally:
        print(f'Постфікс Інструкції: {postfixCode}')
        print(f'Таблиця змінних: {tableOfId}')
        return commandTrack

