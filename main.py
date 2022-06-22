from compiler import lex, tableOfSymb, C2Parser, postfixTranslator, postfixInterpreter, stack

lex()

C2Parser(tableOfSymb).parseProgram()

# run  postfixInterpreter

# print("Запускаю Translator")
# postfixTranslator(tableOfSymb)
print(f">>>{tableOfSymb}")
print("Запускаю Інтерпретер")
postfixInterpreter(tableOfSymb)

# stack.print()