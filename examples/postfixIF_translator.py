from  lex_my_lang_03 import lex, tableToPrint
from  lex_my_lang_03 import tableOfSymb, tableOfId, tableOfConst, tableOfLabel, sourceCode, FSuccess

# FSuccessTr = (False,'Translator')

# lex()
# print('-'*30)
# print('tableOfSymb:{0}'.format(tableOfSymb))
# print('-'*30)

# Список для зберігання ПОЛІЗу - 
# коду у постфіксній формі
postfixCode = []

# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow=1    

# довжина таблиці символів програми 
# він же - номер останнього запису
len_tableOfSymb = 0


toView = False

def postfixTranslator():
    global len_tableOfSymb, FSuccess
    lex()
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
        # перевірити наявність ключового слова 'program'
        parseToken('program','keyword','')  # Трансляція не потрібна
                                            # лексема не має операційної семантики 

        # перевірити синтаксичну коректність списку інструкцій StatementList
        parseStatementList()                # Трансляція (тут нічого не робити)  
                                            # ця функція сама згенерує 
                                            # та додасть ПОЛІЗ інструкцій (виразів)

        # перевірити наявність ключового слова 'end'
        parseToken('end','keyword','')      # Трансляція не потрібна
                                            # лексема не має операційної семантики 

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
    numRow += 1
        
    # чи збігаються лексема та токен таблиці розбору з заданими 
    if (lex, tok) == (lexeme,token):
        # вивести у консоль номер рядка програми та лексему і токен
        # print(indent+'parseToken: В рядку {0} токен {1}'.format(numLine,(lexeme,token)))
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
def parseStatementList():
        # print('\t parseStatementList():')
        while parseStatement():
                pass
        return True


def parseStatement():
    # print('\t\t parseStatement():')
    # прочитаємо поточну лексему в таблиці розбору
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

    elif tok == 'label':
        parseLabel()                        # stub
        return True
    elif (lex, tok) == ('goto','keyword'):
        parseGoto()                         # stub
        return True

    # тут - ознака того, що всі інструкції були коректно 
    # розібрані і була знайдена остання лексема програми.
    # тому parseStatement() має завершити роботу
    elif (lex, tok) == ('end','keyword'):
            return False

    else: 
        # жодна з інструкцій не відповідає 
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій',(numLine,lex,tok,'ident або if'))
        return False


def parseLabel():
    print('-'*20+'Заглушка.  Функція ще не реалізована')
    return True

def parseGoto():
    print('-'*20+'Заглушка.  Функція ще не реалізована')
    return True


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
    numRow += 1

    # print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    # якщо була прочитана лексема - ':='
    if parseToken(':=','assign_op','\t\t\t\t\t'):
        # розібрати арифметичний вираз
        parseExpression()       # Трансляція (тут нічого не робити)  
                                # ця функція сама згенерує 
                                # та додасть ПОЛІЗ виразу       

        postfixCode.append((':=','assign_op'))# Трансляція   
                                # Бінарний оператор  ':='
                                # додається після своїх операндів
        if toView: configToPrint(':=',numRow)
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
        numRow += 1
        parseBoolExpr()                     # Трансляція
        parseToken('then','keyword','\t'*5)
        # Згенерувати мітку m1 = (lex,'label')
        m1 = createLabel()      
        postfixCode.append(m1)  # Трансляція    
        postfixCode.append(('JF','jf'))          
                                # додали m1 JF   
        
        parseStatement()        # Трансляція    

        parseToken('else','keyword','\t'*5)
        # Згенерувати мітку m2 = (lex,'label')
        m2 = createLabel()      
        postfixCode.append(m2)  # Трансляція
        postfixCode.append(('JMP','jump'))  
        setValLabel(m1) # в табл. міток
        postfixCode.append(m1)
        postfixCode.append((':','colon'))
                                # додали m2 JMP m1 :
        parseStatement()        # Трансляція
        parseToken('endif','keyword','\t'*5)
        setValLabel(m2) # в табл. міток
        postfixCode.append(m2)  # Трансляція
        postfixCode.append((':','colon'))
                                # додали m2 JMP m1 :
        return True
    else: return False

def createLabel():
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
        numRow += 1
        postfixCode.append((lex,tok))   # Трансляція
        return True
    else:
        parseExpression()               # Трансляція
        numLine, lex, tok = getSymb()
        numRow += 1
        parseExpression()               # Трансляція
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
        _numLine, lex, tok = getSymb()
        if tok in ('add_op'):
            numRow += 1
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
        _numLine, lex, tok = getSymb()
        if tok in ('mult_op'):
            numRow += 1
            # print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
            parseFactor()       # Трансляція (тут нічого не робити)    
                                # ця функція сама згенерує та додасть ПОЛІЗ множника

                                # Трансляція   
            postfixCode.append((lex,tok))  
                                # lex - бінарний оператор  '*' чи '/'
                                # додається після своїх операндів
            if toView: configToPrint(lex,numRow)
        else:
            F = False
    return True

def parseFactor():
    global numRow, postfixCode
    # print('\t'*7+'parseFactor():')
    numLine, lex, tok = getSymb()
    # print('\t'*7+'parseFactor():=============рядок: {0}\t (lex, tok):{1}'.format(numLine,(lex, tok)))
    
    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    if tok in ('int','float','ident'):
        postfixCode.append((lex,tok))      # Трансляція
                                # ПОЛІЗ константи або ідентифікатора 
                                # відповідна константа або ідентифікатор
        if toView: configToPrint(lex,numRow)

        numRow += 1
        # print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    
    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex=='(':
        numRow += 1
        parseExpression()       # Трансляція (тут нічого не робити)    
                                # ця функція сама згенерує та додасть ПОЛІЗ множника
                                # дужки у ПОЛІЗ НЕ додаємо
        parseToken(')','par_op','\t'*7)
        # print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    else:
        failParse('невідповідність у Expression.Factor',(numLine,lex,tok,'rel_op, int, float, ident або \'(\' Expression \')\''))
    return True

def serv():
    # tableToPrint('All')
    tableToPrint('Label')
    tableToPrint('Id')
    print('\nПочатковий код програми: \n{0}'.format(sourceCode))
    print('\nКод програми у постфіксній формі (ПОЛІЗ): \n{0}'.format(postfixCode)) 
    for lbl in tableOfLabel:
        print('postfixCode[{0}:{1}]={2}'.format(lbl,tableOfLabel[lbl],postfixCode[tableOfLabel[lbl]]))
    return True

# запуск транслятора
postfixTranslator()    

# print('tableOfSymb:{0}'.format(tableOfSymb))
# print('tableOfId:{0}'.format(tableOfId))
# print('tableOfConst:{0}'.format(tableOfConst))
# print('tableOfLabel:{0}'.format(tableOfLabel))

