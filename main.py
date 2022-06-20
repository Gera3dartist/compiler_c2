from compiler import lex, tableOfSymb, C2Parser, postfixTranslator, postfixInterpreter, stack

lex()
print('>>starting parsing')

C2Parser(tableOfSymb).parseProgram()

# run  postfixInterpreter

# print("Запускаю Translator")
# postfixTranslator(tableOfSymb)

print("Запускаю Інтерпретер")
postfixInterpreter(tableOfSymb)

# stack.print()