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
    "<" : "&lt;",
    '>': '&gt;',
    '"': '&quout;',
    '&': '&amp;'
}
class Tokenizer:
    def __init__(self, file_path:str) -> None:

        file = open(file_path)
        self.file_name = file_path.replace("/", '_')
        self.file = ''.join(file.readlines())
        self.char = self.file[0]
        self.file_length = len(self.file)
        self.position = 0
        self.tokens = []

    def skip_whitespace(self) -> None:
        while(self.char == ' '):
            self.nextToken()
        if self.char == '/' and self.peekChar('/'):
            while(self.char != '\n'):
                self.nextToken()
        if self.char == '/' and self.peekChar("*"):
            self.nextToken()
            self.nextToken()
            self.nextToken()
            while self.char != "*" or not self.peekChar('/'):
                self.nextToken()
            self.nextToken()
            self.nextToken()
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
    def peek(self, jump: int = 1) -> str:
        if self.hasMoreTokens():
            return self.file[self.position + jump]
        return ''
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

from collections import deque 
class Compiler:
    def __init__(self, tokens: list[Token], file_path: str):
        self.file_name = file_path.replace("/", '_')
        self.tokens = deque(tokens)
        self.tokens.popleft()
        self.output = ''
    def get_token_type_str(self,tokenType: TokenType):
        return str(tokenType).split('.')[1]
    
    def create_xml_string(self,token: Token, spaces: int) -> None:
        self.output +=( (' '* spaces) + f'  <{self.get_token_type_str(token.tokenType)}> {token.value} </{self.get_token_type_str(token.tokenType)}>\n')

    def compile_class(self):
        self.output += '<class>\n'
        self.output += '<keyword> class </keyword>\n'
        className = self.tokens.popleft()
        self.create_xml_string(className, 0)

        left_bracket = self.tokens.popleft()
        self.create_xml_string(left_bracket, 0)

        self.compile_class_var_dec()

        self.compile_subroutine(2)
        right_bracket = self.tokens.popleft()
        self.create_xml_string(right_bracket, 0)
        self.output += '</class>\n'
    
    def compile_class_var_dec(self, spaces: int = 2):
        while self.tokens and self.tokens[0].value in ['static', 'field']:
            # (static | field) type varName (',' varName)* ';'

            self.output += (' ' * spaces +  f'<classVarDec>\n')
            varDecType = self.tokens.popleft()
            self.create_xml_string(varDecType, spaces)

            varType = self.tokens.popleft()
            self.create_xml_string(varType, spaces)

            varName = self.tokens.popleft()
            self.create_xml_string(varName, spaces)

            while self.tokens and self.tokens[0].value == ',':
                comma = self.tokens.popleft()
                self.create_xml_string(comma, spaces)

                varName = self.tokens.popleft()
                self.create_xml_string(varName, spaces)
            semicolon = self.tokens.popleft()
            self.create_xml_string(semicolon, spaces)
            self.output += (' ' * spaces +  f'</classVarDec>\n' )

    
    def compile_subroutine(self, spaces: int):
        token = self.tokens[0]
        possibleValues = {'constructor', 'function', 'method'}
        if token.value not in  possibleValues:
            return
        
        while self.tokens and self.tokens[0].value in possibleValues:
            self.output += (' ' * spaces +  f'<subroutineDec>\n')
            subRoutineType = self.tokens.popleft()
            self.create_xml_string(subRoutineType,spaces)

            subRoutineReturnType = self.tokens.popleft()
            self.create_xml_string(subRoutineReturnType, spaces)

            subRoutineName = self.tokens.popleft()
            self.create_xml_string(subRoutineName, spaces)
            
            self.compile_paramater_list(spaces * 2)
            self.compile_subroutine_body(spaces * 2)

            self.output += ( ' ' * spaces +  f'</subroutineDec>\n' )

    def compile_paramater_list(self, spaces):
        left_bracket = self.tokens.popleft()
        self.create_xml_string(left_bracket, spaces //2)

        self.output += ( ' ' * spaces + f'<parameterList>\n' )

        while self.tokens[0].value != ')':
            paramType = self.tokens.popleft()
            self.create_xml_string(paramType, spaces)

            paramName = self.tokens.popleft()
            self.create_xml_string(paramName, spaces)

            if self.tokens[0].value == ',':
                comma = self.tokens.popleft()
                self.create_xml_string(comma, spaces)

        self.output += ( ' ' * spaces + f'</parameterList>\n' )
        right_bracket = self.tokens.popleft()
        self.create_xml_string(right_bracket, spaces // 2)

    def compile_subroutine_body(self, spaces):
        self.output +=  ( ' ' * spaces + '<subroutineBody>\n' )
        left_bracket = self.tokens.popleft()
        self.create_xml_string(left_bracket, spaces)

        while self.tokens[0].value == 'var':
            self.compile_var_dec(spaces + 2)


        self.compile_statements(spaces * 2)
        right_bracket = self.tokens.popleft()
        self.create_xml_string(right_bracket, spaces)

        self.output +=  ( ' ' * spaces + '</subroutineBody>\n' )
    
    def compile_var_dec(self, spaces):
        self.output += ( ' ' * spaces +  f'<varDec>\n' )
        var = self.tokens.popleft()
        self.create_xml_string(var, spaces)

        varType = self.tokens.popleft()
        self.create_xml_string(varType, spaces)

        varName = self.tokens.popleft()
        self.create_xml_string(varName,spaces)

        while self.tokens[0].value == ',':
            comma = self.tokens.popleft()
            self.create_xml_string(comma,spaces)

            varName = self.tokens.popleft()
            self.create_xml_string(varName,spaces)      

        semicolon = self.tokens.popleft()
        self.create_xml_string(semicolon,spaces)
        self.output += ( ' ' * spaces +  f'</varDec>\n' )

    def compile_statements(self, spaces):
        self.output +=  ( ' ' * (spaces - 2) + '<statements>\n' )
        if self.tokens[0].value not in ['let', 'while', 'do', 'return', 'if']:
            self.output +=  ( ' ' * (spaces - 2) + '</statements>\n' )
            return
        statments = deque()
        statments.append(self.tokens.popleft())
        statmentsType = {'let', 'while', 'do', 'return', 'if'}
        while statments:
            statement = statments.popleft()
            if statement.value == 'let':
                self.compile_let(spaces, statement)
                if self.tokens[0].value in statmentsType:
                    statments.append(self.tokens.popleft())
            if statement.value == 'while':
                self.compile_while(spaces, statement)
                if self.tokens[0].value in statmentsType:
                    statments.append(self.tokens.popleft())
            if statement.value == 'do':
                self.compile_do(spaces, statement)
                if self.tokens[0].value in statmentsType:
                    statments.append(self.tokens.popleft())
            if statement.value == 'return':
                self.compile_return(spaces, statement)
                if self.tokens[0].value in statmentsType:
                    statments.append(self.tokens.popleft())
            if statement.value == 'if':
                self.compile_if(spaces, statement)
                if self.tokens[0].value in statmentsType:
                    statments.append(self.tokens.popleft())
        self.output +=  ( ' ' * (spaces - 2) + '</statements>\n' )
    def compile_let(self,spaces, token: Token):
        self.output +=  ( ' ' * (spaces) + '<letStatement>\n' )
        let = token
        self.create_xml_string(let, spaces)

        varName = self.tokens.popleft()
        self.create_xml_string(varName, spaces)

        equalSign = self.tokens.popleft()
        self.create_xml_string(equalSign, spaces)

        self.compile_expression(spaces + 2)

        self.output +=  ( ' ' * (spaces) + '</letStatement>\n' )
        
    def compile_if(self, spaces, token: Token):
        self.output +=  ( ' ' * (spaces) + '<ifStatement>\n' )
        self.create_xml_string(token, spaces)

        left_bracket = self.tokens.popleft()
        self.create_xml_string(left_bracket, spaces)

        self.compile_expression(spaces + 2, nonTerminal=False)

        right_bracket = self.tokens.popleft()
        self.create_xml_string(right_bracket, spaces)

        left_square_bracket = self.tokens.popleft()
        self.create_xml_string(left_square_bracket, spaces + 2)


        self.compile_statements(spaces + 2)
        right_sqaure_bracket = self.tokens.popleft()
        self.create_xml_string(right_sqaure_bracket, spaces)

        if self.tokens and self.tokens[0].value == 'else':
            elseToken = self.tokens.popleft()
            self.create_xml_string(elseToken, spaces)

            left_square_bracket = self.tokens.popleft()
            self.create_xml_string(left_square_bracket, spaces + 2)

            self.compile_statements(spaces + 2)
            right_sqaure_bracket = self.tokens.popleft()
            self.create_xml_string(right_sqaure_bracket, spaces)
        
        self.output +=  ( ' ' * (spaces) + '</ifStatement>\n' )

    def compile_while(self, spaces, token: Token):
        self.output +=  ( ' ' * (spaces) + '<whileStatement>\n' )
        self.create_xml_string(token, spaces)

        left_bracket = self.tokens.popleft()
        self.create_xml_string(left_bracket, spaces)

        self.compile_expression(spaces + 2, nonTerminal=False)

        right_bracket = self.tokens.popleft()
        self.create_xml_string(right_bracket, spaces)

        left_square_bracket = self.tokens.popleft()
        self.create_xml_string(left_square_bracket, spaces + 2)

        self.compile_statements(spaces + 2)
        right_sqaure_bracket = self.tokens.popleft()
        self.create_xml_string(right_sqaure_bracket, spaces)

        self.output +=  ( ' ' * (spaces) + '</whileStatement>\n' )

        pass
    def compile_do(self, spaces,token: Token):
        self.output +=  ( ' ' * spaces + '<doStatement>\n' )
        self.create_xml_string(token, spaces)

        self.compile_term(spaces, True)

        semiclon = self.tokens.popleft()
        self.create_xml_string(semiclon, spaces)
        self.output +=  ( ' ' * spaces + '</doStatement>\n' )
    def compile_return(self,spaces, token):
        self.output +=  ( ' ' * spaces + '<returnStatement>\n' )
        self.create_xml_string(token, spaces)

        if self.tokens[0].value != ';':
            self.compile_expression(spaces + 2, nonTerminal=False)

        semiclon = self.tokens.popleft()
        self.create_xml_string(semiclon,spaces)
        self.output +=  ( ' ' * spaces + '</returnStatement>\n' )
        
    def compile_expression(self, spaces, nonTerminal=True):
        self.output +=  ( ' ' * spaces + '<expression>\n' )
        self.compile_term(spaces + 2)

        op = {"&lt;", '=', '+', '/'}
        while self.tokens[0].value in op:
            self.create_xml_string(self.tokens.popleft(), spaces)
            self.compile_term(spaces)
        self.output +=  ( ' ' * spaces + '</expression>\n' )
        if nonTerminal:
            semicolon = self.tokens.popleft()
            self.create_xml_string(semicolon, spaces)
        if self.tokens[0].value in op:
            self.create_xml_string(self.tokens.popleft(), spaces)
            self.compile_expression(spaces + 2)
    def compile_term(self, spaces, subRoutine=False):
        if not subRoutine:
            self.output +=  ( ' ' * spaces + '<term>\n' )
        
        if self.tokens[1].value == '.':
            varNameIdentifier = self.tokens.popleft()
            self.create_xml_string(varNameIdentifier, spaces)

            dot = self.tokens.popleft()
            self.create_xml_string(dot, spaces)

            varNameIdentifier = self.tokens.popleft()
            self.create_xml_string(varNameIdentifier, spaces)

            leftBracket = self.tokens.popleft()
            self.create_xml_string(leftBracket, spaces)
            self.compile_expression_list(spaces + 2)

            rightBracket = self.tokens.popleft()
            self.create_xml_string(rightBracket, spaces)

        elif self.tokens[1].value == '[' :
            identifier = self.tokens.popleft()
            self.create_xml_string(identifier, spaces)
            left_square = self.tokens.popleft()
            self.create_xml_string(left_square, spaces)
            self.compile_expression(spaces + 2, nonTerminal=False)
            right_square = self.tokens.popleft()
            self.create_xml_string(right_square, spaces)
        else:
            stringConstant = self.tokens.popleft()
            self.create_xml_string(stringConstant, spaces)
            
            if self.tokens and self.tokens[0].value == '(':
                leftBracket = self.tokens.popleft()
                self.create_xml_string(leftBracket, spaces)
                self.compile_expression_list(spaces + 2)

                rightBracket = self.tokens.popleft()
                self.create_xml_string(rightBracket, spaces)

        if not subRoutine:
            self.output +=  ( ' ' * spaces + '</term>\n' )
    def compile_expression_list(self, spaces):
        self.output +=  ( ' ' * spaces + '<expressionList>\n' )
        if self.tokens[0].value != ')':
            self.compile_expression(spaces + 2, False)
            while self.tokens[0].value == ',':
                comma = self.tokens.popleft()
                self.create_xml_string(comma, spaces)

                self.compile_expression(spaces + 2, False)
        self.output +=  ( ' ' * spaces + '</expressionList>\n' )
    def print_tokens(self) -> None:
        file = open("parsing_tests" + "/" + self.file_name + 'T_output.xml', 'w')
        file.write(self.output)
        file.close()

if __name__ == "__main__":
    # file_path = sys.argv[1]
    file_path = 'ExpressionLessSquare/Square.jack'
    tokenizer = Tokenizer(file_path)

    while tokenizer.hasMoreTokens():
        tokenizer.advance()
    tokenizer.print_tokens(inConsole=False)
    parser = Compiler(tokenizer.tokens, file_path)
    parser.compile_class()
    parser.print_tokens()


