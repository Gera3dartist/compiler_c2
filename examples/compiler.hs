import Text.Parsec
import Text.Parsec.String
import Text.ParserCombinators.Parsec.Number
import Data.Set (fromList, toList)

{-|
Арифметика: цілі та дійсні числа, основні чотири арифметичні операції
(додавання, віднімання, ділення та множення), піднесення до степеня
(правоасоціативна операція), дужки

Особливості: експоненційна форма дійсного числа
Інструкція повторення: do <список операторів> while <логічний вираз>
Інструкція розгалуження: if (<відношення>) {<блок операторів>}
-}


type Var = String
data Statement = Print Var | Assign Var Int | Add Var Var | While Var Code  deriving (Eq, Show)
type Code = [Statement]

-- part 1. parser - String (input.txt) -> Code
statementParser :: Parser Statement
statementParser = try printParser <|> try assignParser <|> try addParser <|> whileParser

printParser :: Parser Statement
printParser = Print <$> (string "print" >> many1 space >> many1 letter)

assignParser :: Parser Statement
assignParser = Assign <$> (many1 letter) <*> (many1 space >> char '=' >> many1 space >> int)

addParser :: Parser Statement
addParser = Add <$> (many1 letter) <*> (many1 space >> string "+=" >> many1 space >> many1 letter)

whileParser :: Parser Statement
whileParser = While <$> (string "while" >> many1 space >> many1 letter) <*> (many1 space >> string "positive" >> many1 space >> char '{' >> many1 space >> many (statementParser <* many1 space) <* char '}')

codeParser :: Parser Code
codeParser = spaces >> many (statementParser <* many1 space) <* eof

-- part 2. code generator - Code -> String (output.c)
statementToC :: Statement -> String
statementToC (Assign v n) = v ++ " = " ++ show n ++ ";"
statementToC (Add a b) = a ++ " += " ++ b ++ ";"
statementToC (Print v) = "printf(\"%d\\n\", " ++ v ++ ");"
statementToC (While v c) = "while (" ++ v ++ " > 0) {\n" ++ statementsToC c ++ "}"

statementsToC :: [Statement] -> String
statementsToC stmts = unlines (map statementToC stmts)

statementVariables :: Statement -> [Var]
statementVariables (Print v) = [v]
statementVariables (Assign v n) = [v]
statementVariables (Add a b) = [a,b]
statementVariables (While v c) = [v] ++ statementsVariables c

statementsVariables :: [Statement] -> [Var]
statementsVariables stmts = concat (map statementVariables stmts)

codeVariables :: [Statement] -> [Var]
codeVariables code = toList (fromList (statementsVariables code))

makeDeclaration :: Var -> String
makeDeclaration v = "int " ++ v ++ ";"

makeDeclarations :: [Var] -> String
makeDeclarations vs = unlines (map makeDeclaration vs)

codeToC :: Code -> String
codeToC code = "#include <stdio.h>\nint main() {\n" ++ makeDeclarations (codeVariables code) ++ statementsToC code ++ "return 0;\n}"

main = do
  fileText <- readFile "input.txt"
  let parsed = parse codeParser "input.txt" fileText
  case parsed of
    Left e -> print e
    Right c -> writeFile "output.c" (codeToC c)
