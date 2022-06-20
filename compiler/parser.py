import typing as t


class C2Parser:
    def __init__(self, table_of_symb: dict):
        self.numRow = 1
        self.table_of_symb = table_of_symb
        self.len_table_of_symb=len(table_of_symb)


    def parseProgram(self) -> t.Optional[bool]:
        """
        Функція є вхідною точкою для парсингу програми
        Програма представлена як набір інструкцій
        """
        try:

            # перевірити синтаксичну коректність списку інструкцій StatementList
            self.parseStatementList()
            # повідомити про синтаксичну коректність програми
            print('Parser: Синтаксичний аналіз завершився успішно')
            return True
        except SystemExit as e:
            # Повідомити про факт виявлення помилки
            print('Parser: Аварійне завершення програми з кодом {0}'.format(e))

       
    def parseToken(self, lexeme: str, token: str, indent: str)  -> t.Optional[bool]:
        """
        Функція перевіряє, чи у поточному рядку таблиці розбору
        зустрілась вказана лексема lexeme з токеном token
        параметр indent - відступ при виведенні у консоль

        """
        # якщо всі записи таблиці розбору прочитані,
        # а парсер ще не знайшов якусь лексему
        if self.numRow > self.len_table_of_symb :
            self.failParse('неочікуваний кінець програми',(lexeme,token,self.numRow))
            
        # прочитати з таблиці розбору 
        # номер рядка програми, лексему та її токен
        numLine, lex, tok = self.getSymb() 
            
        # тепер поточним буде наступний рядок таблиці розбору
        self.numRow += 1
            
        # чи збігаються лексема та токен таблиці розбору з заданими 
        if (lex, tok) == (lexeme,token):
            # вивести у консоль номер рядка програми та лексему і токен
            print(indent+'parseToken: В рядку {0} токен {1}'.format(numLine,(lexeme,token)))
            return True
        else:
            # згенерувати помилку та інформацію про те, що 
            # лексема та токен таблиці розбору (lex,tok) відрізняються від
            # очікуваних (lexeme,token)
            self.failParse('невідповідність токенів',(numLine,lex,tok,lexeme,token))
            return False


   
    def getSymb(self, numRow: t.Optional[int] = None) -> t.Tuple[int, str, str]:
        """
        Прочитати з таблиці розбору поточний запис
        Повертає номер рядка програми, лексему та її токен
        """
        numRow = numRow or self.numRow
        if numRow > self.len_table_of_symb:
            self.failParse('getSymb(): неочікуваний кінець програми', numRow)
        # таблиця розбору реалізована у формі словника (dictionary)
        # len_table_of_symb[self.numRow]={self.numRow: (numLine, lexeme, token, indexOfVarOrConst)
        numLine, lexeme, token, _ = self.table_of_symb[numRow]	
        return numLine, lexeme, token        

    def failParse(self, str: str, tuple: tuple) -> None:
        """
        Обробити помилки
        вивести поточну інформацію та діагностичне повідомлення 
        """
        if str == 'неочікуваний кінець програми':
            (lexeme,token,self.numRow)=tuple
            print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format((lexeme,token),self.numRow))
            exit(1001)
        if str == 'getSymb(): неочікуваний кінець програми':
            self.numRow=tuple
            print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(self.numRow,self.len_table_of_symb[self.numRow-1]))
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
        
    def parseStatementList(self) -> bool:
        """
        Функція для розбору за правилом для StatementList 
        StatementList = Statement  { Statement }
        викликає функцію parseStatement() доти,
        доки parseStatement() повертає True
        """
        print('\t parseStatementList():')
        while self.parseStatement():
                pass
        return True


    def parseStatement(self) -> bool:
        """
        Метод для розбору за правилом для 
        Statement = Assign | Expression;
        """
        print('\t\t parseStatement():')
        # прочитаємо поточну лексему в таблиці розбору
        if self.numRow > self.len_table_of_symb:
            return False
        numLine, lex, tok = self.getSymb()
        # якщо токен - ідентифікатор
        # обробити інструкцію присвоюванн
        if tok == 'ident':    
            self.parseAssign()
            return True

        # якщо лексема - ключове слово 'if'
        # обробити інструкцію розгалудження
        elif (lex, tok) == ('if','keyword'):
            self.parseIf()
            return True 
        elif (lex, tok) == ('do','keyword'):
            self.parseDoWhile()
            return True 
        elif (lex, tok) == ('}','curbr_op'):
            # hit code block
            return False

        # тут - ознака того, що всі інструкції були коректно 
        # розібрані і була знайдена остання лексема програми.
        # тому parseStatement() має завершити роботу
        
        else: 
            # жодна з інструкцій не відповідає 
            # поточній лексемі у таблиці розбору,
            self.failParse('невідповідність інструкцій',(numLine,lex,tok,'ident або if'))
            return False


    def parseAssign(self) -> bool:
        """
        Метод для розбору конструкції Assign
        Assign = Variable, "=", Expression;
        """
        # номер запису таблиці розбору
        print('\t'*4+'parseAssign():')

        # взяти поточну лексему
        numLine, lex, tok = self.getSymb()

        # встановити номер нової поточної лексеми
        self.numRow += 1

        print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
        # якщо була прочитана лексема - '='
        if self.parseToken('=','assign_op','\t\t\t\t\t'):
            # розібрати арифметичний вираз
            self.parseExpression()
            return True
        else: return False    


    def parseExpression(self) -> bool:
        """
        Метод для розбору конструкції Expression
        Expression = ArithmExpression | BoolExpr
        """
        print('\t'*5+'parseExpression():')
        numLine, lex, tok = self.getSymb()
        self.parseTerm()
        F = True
        # продовжувати розбирати Доданки (Term)
        # розділені лексемами '+' або '-'
        while F:

            if self.numRow > self.len_table_of_symb:
                break
            numLine, lex, tok = self.getSymb()
            if tok in ('add_op', 'rel_op'):
                self.numRow += 1
                print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
                self.parseTerm()
            else:
                F = False
        return True

    def parseTerm(self) -> bool:
        """
        Метод для розбору конструкції Term
        Term = Factor 
        | Term, "*", Factor 
        | Term, "/", Factor 
        | Term, "^", Factor

        """
        print('\t'*6+'parseTerm():')
        self.parseFactor()
        F = True
        # продовжувати розбирати Множники (Factor)
        # розділені лексемами '*' або '/'
        while F:
            if self.numRow > self.len_table_of_symb:
                break
            numLine, lex, tok = self.getSymb()
            if tok in ('mult_op', ):
                self.numRow += 1
                print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
                self.parseFactor()
            else:
                F = False
        return True

    def parseFactor(self) -> bool:
        """
        Метод для розбору конструкції Factor
        Factor = Variable 
            | Const 
            | "(", ArithmExpression, ")"; 
        """
        print('\t'*7+'parseFactor():')
        numLine, lex, tok = self.getSymb()
        print('\t'*7+'parseFactor():=============рядок: {0}\t (lex, tok):{1}'.format(numLine,(lex, tok)))
        
        # перша і друга альтернативи для Factor
        # якщо лексема - це константа або ідентифікатор
        if tok in ('int','float','ident'):
                self.numRow += 1
                print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
        
        # третя альтернатива для Factor
        # якщо лексема - це відкриваюча дужка
        elif lex=='(':
            self.numRow += 1
            self.parseExpression()
            self.parseToken(')','par_op','\t'*7)
            print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
        else:
            self.failParse('невідповідність у Expression.Factor',(numLine,lex,tok,'rel_op, int, float, ident або \'(\' Expression \')\''))
        return True

    def parseIf(self) -> bool:
        """
        розбір інструкції розгалудження за правилом
        IfStatement = "if", ["("], BoolExpr,  [")"], CodeBlock, "else", CodeBlock
        функція названа parseIf() замість parseIfStatement()
        """

        _, lex, tok = self.getSymb()
        if lex=='if' and tok=='keyword':
            self.numRow+=1
            self.parseExpression()
            self.parseCodeBlock()
            if self.parseToken('else','keyword','\t'*7):
                self.parseCodeBlock()
            return True
        else: return False

    def parseCodeBlock(self) -> bool:
        """
        розбір конструкції код блок
        CodeBlock = "{", {Newline}  StatementList, {Newline}, "}";
        """
        numLine, lex, tok = self.getSymb()

        if lex== '{':
            self.numRow += 1
            self.parseStatementList();
            self.parseToken('}','curbr_op','\t'*7)
            print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
        else:
            self.failParse('mismatch in CodeBlock',(numLine,lex,tok, 'curbr_op'))
        return True

    def parseDoWhile(self) -> bool:
        """
        розбір інструкції do while
        doWhileStatement = "do", CodeBlock, "while", BoolExpr;
        """
        _, lex, tok = self.getSymb()
        if lex=='do' and tok=='keyword':
            self.numRow+=1
            self.parseCodeBlock()
            self.parseToken('while','keyword','\t'*7)
            self.parseExpression()
            return True
        else: return False
