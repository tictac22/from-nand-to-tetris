import os
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
        self.file_length = len(self.file)
        self.position = 0
        self.char = self.file[0] if self.file_length > 0 else ''
        self.tokens = []

    def skip_whitespace(self) -> None:
        while self.hasMoreTokens():
            if self.char.isspace():
                self.nextToken()
                continue
            if self.char == '/' and self.peekChar('/'):
                while self.hasMoreTokens() and self.char != '\n':
                    self.nextToken()
                continue
            if self.char == '/' and self.peekChar("*"):
                self.nextToken()
                self.nextToken()
                while self.hasMoreTokens() and not (self.char == "*" and self.peekChar('/')):
                    self.nextToken()
                if self.hasMoreTokens():
                    self.nextToken()
                if self.hasMoreTokens():
                    self.nextToken()
                continue
            break
    def advance(self) -> None:
        self.skip_whitespace()
        if not self.hasMoreTokens():
            return
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
        return self.position < self.file_length

    def nextToken(self) -> None:
        self.position += 1
        if self.position < self.file_length:
            self.char = self.file[self.position]
        else:
            self.char = ''

    def prevToken(self) -> None:
        self.position -= 1
        self.char = self.file[self.position]
    def is_letter(self, char: str) -> bool:
        return char.isalpha() or char == '_'
    def tokenType(self) -> None:
        pass
    def get_string(self) -> str:
        output = ''
        while (self.char.isalnum() or self.char == '_'):
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
        if self.position + jump < self.file_length:
            return self.file[self.position + jump]
        return ''
    def peekChar(self, char: str) -> bool:
        if self.position + 1 >= self.file_length:
            return False
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

        op = {"&lt;", '=', '+', '/', '*', '|', '-', '&amp;', '>', '&gt;'}
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

        elif self.tokens[0].value == '(':
            leftBracket = self.tokens.popleft()
            self.create_xml_string(leftBracket, spaces)

            self.compile_expression(spaces + 2, nonTerminal=False)

            rightBracket = self.tokens.popleft()
            self.create_xml_string(rightBracket, spaces)
        elif self.tokens[0].value in ['-', '~']:
            unaryOp = self.tokens.popleft()
            self.create_xml_string(unaryOp, spaces)
            self.compile_term(spaces + 2, subRoutine=False)
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



class SymbolTable:
    def __init__(self) -> None:
        self.class_scope = {}
        self.subroutine_scope = {}
        self.count = {'static': 0,
            'field': 0,
            'arg': 0,
            'var': 0
        }
    def startSubroutine(self):
        self.subroutine_scope = {}
        self.count['arg'] = 0
        self.count['var'] = 0
    def define(self, name: str, type: str, kind: str):
        if kind in ['static', 'field']:
            self.class_scope[name] = (type, kind, self.count[kind])
        else:
            self.subroutine_scope[name] = (type, kind, self.count[kind])
        self.count[kind] += 1
    def varCount(self, kind: str) -> int:
        return self.count[kind]
    def kindOf(self, name: str) -> str:
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][1]
        if name in self.class_scope:
            return self.class_scope[name][1]
        return 'none'

    def typeOf(self, name: str) -> str:
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][0]
        if name in self.class_scope:
            return self.class_scope[name][0]
        return 'none'
    def indexOf(self, name: str) -> int:
        if name in self.subroutine_scope:
            return self.subroutine_scope[name][2]
        if name in self.class_scope:
            return self.class_scope[name][2]
        return 'none'

class VMWriter:
    def __init__(self, file_path: str) -> None:
        self.file_name = file_path.replace("/", '_')
        self.file_path = file_path
        self.output = ''
    def writePush(self, segment: str, index: int):
        self.output += f'push {segment} {index}\n'
    def writePop(self, segment: str, index: int):
        self.output += f'pop {segment} {index}\n'
    def writeArithmetic(self, command: str):
        self.output += f'{command}\n'
    def writeLabel(self, label: str):
        self.output += f'label {label}\n'
    def writeGoto(self, label: str):
        self.output += f'goto {label}\n'
    def writeIf(self, label: str):
        self.output += f'if-goto {label}\n'
    def writeCall(self, name: str, nArgs: int):
        self.output += f'call {name} {nArgs}\n'
    def writeFunction(self, name: str, nLocals: int):
        self.output += f'function {name} {nLocals}\n'
    def writeReturn(self):
        self.output += 'return\n'
    def print_tokens(self) -> None:
        output_path = self.file_path.replace('.jack', '.vm')
        file = open(output_path, 'w')
        file.write(self.output)
        file.close()

class Compiler2:
    def __init__(self, tokens: list[Token], file_path: str):
        self.file_name = file_path.replace("/", '_')
        self.tokens = deque(tokens)
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(file_path)
        self.className = ''
        self.labelCounter = 0

    def _normalize(self, value: str) -> str:
        return {'&lt;': '<', '&gt;': '>', '&amp;': '&', '&quout;': '"'}.get(value, value)

    def _current(self) -> Token:
        return self.tokens[0]

    def _peek(self, offset: int = 1) -> Token:
        return self.tokens[offset]

    def _current_value(self) -> str:
        return self._normalize(self._current().value)

    def _peek_value(self, offset: int = 1) -> str:
        return self._normalize(self._peek(offset).value)

    def _eat(self, expected: str | None = None) -> Token:
        token = self.tokens.popleft()
        current_value = self._normalize(token.value)
        if expected is not None and current_value != expected:
            raise ValueError(f"Expected '{expected}', got '{current_value}'")
        return token

    def _eat_identifier(self) -> str:
        token = self._eat()
        if token.tokenType != TokenType.identifier:
            raise ValueError(f"Expected identifier, got '{token.value}'")
        return token.value

    def _segment_of_kind(self, kind: str) -> str:
        return {
            'static': 'static',
            'field': 'this',
            'arg': 'argument',
            'var': 'local',
        }[kind]

    def _push_var(self, name: str):
        kind = self.symbolTable.kindOf(name)
        index = self.symbolTable.indexOf(name)
        if kind == 'none' or index == 'none':
            raise ValueError(f"Unknown variable '{name}'")
        self.vmWriter.writePush(self._segment_of_kind(kind), index)

    def _pop_var(self, name: str):
        kind = self.symbolTable.kindOf(name)
        index = self.symbolTable.indexOf(name)
        if kind == 'none' or index == 'none':
            raise ValueError(f"Unknown variable '{name}'")
        self.vmWriter.writePop(self._segment_of_kind(kind), index)

    def _new_label(self, prefix: str) -> str:
        label = f"{self.className}.{prefix}.{self.labelCounter}"
        self.labelCounter += 1
        return label

    def _write_op(self, op: str):
        if op == '+':
            self.vmWriter.writeArithmetic('add')
        elif op == '-':
            self.vmWriter.writeArithmetic('sub')
        elif op == '&':
            self.vmWriter.writeArithmetic('and')
        elif op == '|':
            self.vmWriter.writeArithmetic('or')
        elif op == '<':
            self.vmWriter.writeArithmetic('lt')
        elif op == '>':
            self.vmWriter.writeArithmetic('gt')
        elif op == '=':
            self.vmWriter.writeArithmetic('eq')
        elif op == '*':
            self.vmWriter.writeCall('Math.multiply', 2)
        elif op == '/':
            self.vmWriter.writeCall('Math.divide', 2)

    def compile_class(self):
        self._eat('class')
        self.className = self._eat_identifier()
        self._eat('{')
        self.compile_class_var_dec()
        self.compile_subroutine(0)
        self._eat('}')

    def compile_class_var_dec(self, spaces: int = 0):
        while self.tokens and self._current_value() in ['static', 'field']:
            varDecType = self._eat().value
            varType = self._eat().value
            varName = self._eat_identifier()
            self.symbolTable.define(varName, varType, varDecType)
            while self.tokens and self._current_value() == ',':
                self._eat(',')
                varName = self._eat_identifier()
                self.symbolTable.define(varName, varType, varDecType)
            self._eat(';')

    def compile_subroutine(self, spaces: int):
        possibleValues = {'constructor', 'function', 'method'}
        while self.tokens and self._current_value() in possibleValues:
            self.symbolTable.startSubroutine()

            subroutineType = self._eat().value
            self._eat()  # return type
            subroutineName = self._eat_identifier()

            if subroutineType == 'method':
                self.symbolTable.define('this', self.className, 'arg')

            self._eat('(')
            self.compile_paramater_list(0)
            self._eat(')')

            self._eat('{')
            nLocals = 0
            while self._current_value() == 'var':
                nLocals += self.compile_var_dec(0)

            self.vmWriter.writeFunction(f'{self.className}.{subroutineName}', nLocals)
            if subroutineType == 'constructor':
                fieldCount = self.symbolTable.varCount('field')
                self.vmWriter.writePush('constant', fieldCount)
                self.vmWriter.writeCall('Memory.alloc', 1)
                self.vmWriter.writePop('pointer', 0)
            elif subroutineType == 'method':
                self.vmWriter.writePush('argument', 0)
                self.vmWriter.writePop('pointer', 0)

            self.compile_statements(0)
            self._eat('}')

    def compile_paramater_list(self, spaces):
        if self._current_value() == ')':
            return

        paramType = self._eat().value
        paramName = self._eat_identifier()
        self.symbolTable.define(paramName, paramType, 'arg')
        while self._current_value() == ',':
            self._eat(',')
            paramType = self._eat().value
            paramName = self._eat_identifier()
            self.symbolTable.define(paramName, paramType, 'arg')

    def compile_var_dec(self, spaces) -> int:
        self._eat('var')
        varType = self._eat().value
        count = 0

        varName = self._eat_identifier()
        self.symbolTable.define(varName, varType, 'var')
        count += 1
        while self._current_value() == ',':
            self._eat(',')
            varName = self._eat_identifier()
            self.symbolTable.define(varName, varType, 'var')
            count += 1
        self._eat(';')
        return count

    def compile_statements(self, spaces):
        while self.tokens and self._current_value() in ['let', 'while', 'do', 'return', 'if']:
            statementType = self._current_value()
            if statementType == 'let':
                self.compile_let(spaces, self._eat('let'))
            elif statementType == 'while':
                self.compile_while(spaces, self._eat('while'))
            elif statementType == 'do':
                self.compile_do(spaces, self._eat('do'))
            elif statementType == 'return':
                self.compile_return(spaces, self._eat('return'))
            elif statementType == 'if':
                self.compile_if(spaces, self._eat('if'))

    def compile_let(self,spaces, token: Token):
        varName = self._eat_identifier()
        isArrayAssign = False
        if self._current_value() == '[':
            isArrayAssign = True
            self._push_var(varName)
            self._eat('[')
            self.compile_expression(spaces + 2, nonTerminal=False)
            self._eat(']')
            self.vmWriter.writeArithmetic('add')

        self._eat('=')
        self.compile_expression(spaces + 2, nonTerminal=False)
        self._eat(';')

        if isArrayAssign:
            self.vmWriter.writePop('temp', 0)
            self.vmWriter.writePop('pointer', 1)
            self.vmWriter.writePush('temp', 0)
            self.vmWriter.writePop('that', 0)
        else:
            self._pop_var(varName)
        
    def compile_if(self, spaces, token: Token):
        trueLabel = self._new_label('IF_TRUE')
        falseLabel = self._new_label('IF_FALSE')
        endLabel = self._new_label('IF_END')

        self._eat('(')
        self.compile_expression(spaces + 2, nonTerminal=False)
        self._eat(')')
        self.vmWriter.writeIf(trueLabel)
        self.vmWriter.writeGoto(falseLabel)
        self.vmWriter.writeLabel(trueLabel)

        self._eat('{')
        self.compile_statements(spaces + 2)
        self._eat('}')

        if self.tokens and self._current_value() == 'else':
            self.vmWriter.writeGoto(endLabel)
            self.vmWriter.writeLabel(falseLabel)
            self._eat('else')
            self._eat('{')
            self.compile_statements(spaces + 2)
            self._eat('}')
            self.vmWriter.writeLabel(endLabel)
        else:
            self.vmWriter.writeLabel(falseLabel)

    def compile_while(self, spaces, token: Token):
        expLabel = self._new_label('WHILE_EXP')
        endLabel = self._new_label('WHILE_END')

        self.vmWriter.writeLabel(expLabel)
        self._eat('(')
        self.compile_expression(spaces + 2, nonTerminal=False)
        self._eat(')')
        self.vmWriter.writeArithmetic('not')
        self.vmWriter.writeIf(endLabel)

        self._eat('{')
        self.compile_statements(spaces + 2)
        self._eat('}')
        self.vmWriter.writeGoto(expLabel)
        self.vmWriter.writeLabel(endLabel)

    def compile_do(self, spaces,token: Token):
        self.compile_subroutine_call()
        self._eat(';')
        self.vmWriter.writePop('temp', 0)

    def compile_return(self,spaces, token):
        if self._current_value() != ';':
            self.compile_expression(spaces + 2, nonTerminal=False)
        else:
            self.vmWriter.writePush('constant', 0)
        self._eat(';')
        self.vmWriter.writeReturn()
        
    def compile_expression(self, spaces, nonTerminal=True):
        self.compile_term(spaces + 2)
        op = {'=', '+', '/', '*', '|', '-', '&', '>', '<'}
        while self.tokens and self._current_value() in op:
            curOp = self._eat().value
            self.compile_term(spaces)
            self._write_op(self._normalize(curOp))

    def compile_term(self, spaces, subRoutine=False):
        token = self._current()
        currentValue = self._current_value()

        if token.tokenType == TokenType.integerConstant:
            self.vmWriter.writePush('constant', int(token.value))
            self._eat()
            return

        if token.tokenType == TokenType.stringConstant:
            self.vmWriter.writePush('constant', len(token.value))
            self.vmWriter.writeCall('String.new', 1)
            for ch in token.value:
                self.vmWriter.writePush('constant', ord(ch))
                self.vmWriter.writeCall('String.appendChar', 2)
            self._eat()
            return

        if token.tokenType == TokenType.keyword:
            if currentValue == 'true':
                self.vmWriter.writePush('constant', 0)
                self.vmWriter.writeArithmetic('not')
                self._eat()
                return
            if currentValue in ('false', 'null'):
                self.vmWriter.writePush('constant', 0)
                self._eat()
                return
            if currentValue == 'this':
                self.vmWriter.writePush('pointer', 0)
                self._eat()
                return

        if currentValue == '(':
            self._eat('(')
            self.compile_expression(spaces + 2, nonTerminal=False)
            self._eat(')')
            return

        if currentValue in ['-', '~']:
            unaryOp = self._eat().value
            self.compile_term(spaces + 2, subRoutine=False)
            if self._normalize(unaryOp) == '-':
                self.vmWriter.writeArithmetic('neg')
            else:
                self.vmWriter.writeArithmetic('not')
            return

        if token.tokenType == TokenType.identifier:
            nextValue = self._peek_value()
            if nextValue == '[':
                varName = self._eat_identifier()
                self._push_var(varName)
                self._eat('[')
                self.compile_expression(spaces + 2, nonTerminal=False)
                self._eat(']')
                self.vmWriter.writeArithmetic('add')
                self.vmWriter.writePop('pointer', 1)
                self.vmWriter.writePush('that', 0)
                return

            if nextValue in ['(', '.']:
                self.compile_subroutine_call()
                return

            self._push_var(self._eat_identifier())
            return

        raise ValueError(f"Unexpected token in term: {token.value}")

    def compile_subroutine_call(self):
        firstName = self._eat_identifier()
        argsCount = 0

        if self._current_value() == '.':
            self._eat('.')
            secondName = self._eat_identifier()
            kind = self.symbolTable.kindOf(firstName)
            if kind != 'none':
                self._push_var(firstName)
                argsCount += 1
                className = self.symbolTable.typeOf(firstName)
                callName = f'{className}.{secondName}'
            else:
                callName = f'{firstName}.{secondName}'
        else:
            self.vmWriter.writePush('pointer', 0)
            argsCount += 1
            callName = f'{self.className}.{firstName}'

        self._eat('(')
        argsCount += self.compile_expression_list(0)
        self._eat(')')
        self.vmWriter.writeCall(callName, argsCount)

    def compile_expression_list(self, spaces) -> int:
        argsCount = 0
        if self._current_value() != ')':
            self.compile_expression(spaces + 2, False)
            argsCount += 1
            while self._current_value() == ',':
                self._eat(',')
                self.compile_expression(spaces + 2, False)
                argsCount += 1
        return argsCount

    def print_tokens(self) -> None:
        self.vmWriter.print_tokens()


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'compiler/11/Average/Main.jack'
    if os.path.isdir(file_path):
        for entry in sorted(os.listdir(file_path)):
            if not entry.endswith('.jack'):
                continue
            jack_path = os.path.join(file_path, entry)
            tokenizer = Tokenizer(jack_path)
            while tokenizer.hasMoreTokens():
                tokenizer.advance()
            parser = Compiler2(tokenizer.tokens, jack_path)
            parser.compile_class()
            parser.print_tokens()
    else:
        tokenizer = Tokenizer(file_path)
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
        parser = Compiler2(tokenizer.tokens, file_path)
        parser.compile_class()
        parser.print_tokens()
