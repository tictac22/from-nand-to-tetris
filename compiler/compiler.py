import sys
from enum import Enum

class TokenType(Enum):
    keyword = 1
    symbol = 2
    integerConstant = 3
    stringConstant = 4
    identifier = 5

class Token:
    def __init__(self, tokenType: TokenType, value: str) -> None:
        self.tokenType = tokenType
        self.value = value

keywords = {"class", "constructor", "function", "method", 
            "field", "static", "var", "int", "char", "boolean", "void", 
            "true", "false", "null", "this", "let", "do", "if", 
            "else", "while", "return"
}
xml_symbols = {
    "<" : "&lt;"
}
class Tokenizer:
    def __init__(self, file_path:str) -> None:

        file = open(file_path)
        self.file_name = file_path.split("/")[1].split('.')[0]
        self.file = ''.join(file.readlines())
        self.char = self.file[0]
        self.file_length = len(self.file)
        self.position = 0
        self.tokens = []

    def skip_whitespace(self) -> None:
        if self.char == '/' and (self.peekChar('/') or self.peekChar('*')):
            while(self.char != '\n'):
                self.nextToken()
        while(self.char == ' '):
            self.nextToken()
        pass 
    def advance(self) -> None:
        self.skip_whitespace()
        current_char = self.char
        token = None
        if current_char == '{' or current_char == '}' or current_char == '(' or current_char == ')' or \
            current_char == '[' or current_char == ']' or current_char == '.' or current_char == ',' or \
            current_char == ';' or current_char == '+' or current_char == '-' or current_char == '*' or \
            current_char == '/' or current_char == '&' or current_char == '|' or current_char == '<' or \
            current_char == '>' or current_char == '=' or current_char == '~':
                if current_char in xml_symbols:
                    token = Token(TokenType.symbol, xml_symbols[current_char])
                else:
                    token = Token(TokenType.symbol, current_char)
        elif current_char == '"':
            substring =  ''
            self.nextToken()
            start_position = self.position
            offset = 0
            while (self.char != '"'):
                self.nextToken()
                offset += 1
            substring = self.file[start_position: start_position + offset]
            token = Token(TokenType.stringConstant, substring)
        else:
            if(self.is_letter(self.char)):
                substring = self.get_string()
                if substring in keywords:
                    token = Token(TokenType.keyword, substring)
                elif substring != '':
                    token = Token(TokenType.identifier, substring)
            elif self.char.isnumeric():
                number = self.get_number()
                token = Token(TokenType.integerConstant, number)
        if token:
            self.tokens.append(token)
        self.nextToken()
            
    def hasMoreTokens(self) -> bool:
        return self.position < self.file_length - 1

    def nextToken(self) -> None:
        if not self.hasMoreTokens():
            return
        self.position += 1
        self.char = self.file[self.position]

    def prevToken(self) -> None:
        self.position -= 1
        self.char = self.file[self.position]
    def is_letter(self, char: str) -> bool:
        return 'a' <= char and char <= 'z' or  'A' <= char and 'A' <= char and char <= "Z"
    def tokenType(self) -> None:
        pass
    def get_string(self) -> str:
        output = ''
        while (self.is_letter(self.char)):
            output += self.char
            self.nextToken()
        if output != '':
            self.prevToken()
        return output   
    def get_number(self) -> str:
        output = ''
        while (self.char.isnumeric()):
            output += self.char
            self.nextToken()
        if output != '':
            self.prevToken()
        return output   
    def peekChar(self, char: str) -> bool:
        return self.file[self.position + 1] == char

    def print_tokens(self, inConsole:bool = True) -> None:
        if inConsole:
            print("<tokens>")
        output = '<tokens>\n'
        for token in self.tokens:
            type_name = str(token.tokenType).split(".")[1]
            string = "<" + str(type_name) + ">" + " " + token.value + ' ' + "</" + str(type_name) + '>'
            if inConsole:
                print(string)
            output += (string + "\n")
        output = output + "</tokens>\n"
        file = open("lexer_tests" + "/" + self.file_name + 'T_output.xml', 'w')
        file.write(output)
        file.close()
        if inConsole:
            print("</tokens>")

if __name__ == "__main__":
    file_path = sys.argv[1]
    tokenizer = Tokenizer(file_path)

    while tokenizer.hasMoreTokens():
        tokenizer.advance()
    tokenizer.print_tokens()


