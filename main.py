from compiler import lex, tableOfSymb, C2Parser, postfixTranslator, postfixInterpreter, stack

print("Розпочинаю фазу лексичного аналізу...")
lex()
print("Фаза лексичного аналізу завершилась успішно")

print("Розпочинаю фазу синктаксичного аналізу...")
C2Parser(tableOfSymb).parseProgram()
print("Фаза синктаксичного аналізу завершилась успішно")

print("Запускаю Інтерпретер")
postfixInterpreter(tableOfSymb)

# stack.print()