
from enum import Enum
import sys
class CommandType(Enum):
    C_ARITHMETIC = 0 # arithmetic command
    C_PUSH = 1 # push command
    C_POP = 2 # pop command
    C_LABEL = 3 # label command
    C_GOTO = 4 # goto command
    C_IF = 5 # if-goto command
    C_FUNCTION = 6 # function command
    C_RETURN = 7 # return command
    C_CALL = 8 # call command
    C_ADD = 9
    C_SUB = 10
    C_NEG = 11
    C_EQ = 12
    C_GT = 13
    C_LT = 14
    C_AND = 15
    C_OR = 16
    C_NOT = 17

class Parser:
    def __init__(self, file_name: str):
        self.file = open(file_name, 'r')
        self.line = ''
        self.advance()

    def get_line(self) -> str:
        return self.line
    def has_command(self) -> bool:
        return bool(self.line)
    def advance(self) -> None:
        self.line = self.file.readline().strip().replace('\n','')
    def skip_white_space(self) -> None:
        while(self.line == '' or '//' in self.line):
            self.advance()
    def command_type(self) -> CommandType:
        if "push" in self.line:
            return CommandType.C_PUSH
        if "pop" in self.line:
            return CommandType.C_POP
        if "add" in self.line:
            return CommandType.C_ADD


class CodeWriter:
    def __init__(self, file_output_name:str):
        self.file = open(file_output_name,'w')

    def load_base(self) -> None:
        self.file.write("@256\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")

    def write_command(self, commandType: CommandType, command_line: str) -> None:
        file = self.file
        if commandType == CommandType.C_PUSH:
            if "constant" in command_line:
                number = command_line.split(" ")[-1]
                file.write("//push command\n")
                file.write(f"@{number}\n")
                file.write("D=A\n")
                file.write("@SP\n")
                file.write("A=M\n")
                file.write("M=D\n")
                file.write("@SP\n")
                file.write("M=M+1\n")
        elif commandType == CommandType.C_ADD:
                file.write("//Add command\n")
                file.write("@SP\n")
                file.write("AM=M-1\n")
                file.write("D=M\n")
                file.write("A=A-1\n")
                file.write("M=D+M\n")
file_name = sys.argv[1]
parser = Parser(file_name)
codeWriter = CodeWriter(file_name.split('.')[0] + '.asm')
codeWriter.load_base()
while parser.has_command():
    parser.skip_white_space()
    codeWriter.write_command(parser.command_type(), parser.get_line())
    parser.advance()

parser.file.close()
codeWriter.file.close()