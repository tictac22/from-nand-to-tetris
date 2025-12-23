
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
        if "eq" in self.line:
            return CommandType.C_EQ
        if "lt" in self.line:
            return CommandType.C_LT
        if "gt" in self.line:
            return CommandType.C_GT
        if "add" in self.line:
            return CommandType.C_ADD
        if "sub" in self.line:
            return CommandType.C_SUB
        if "neg" in self.line:
            return CommandType.C_NEG
        if "and" in self.line:
            return CommandType.C_AND
        if "or" in self.line:
            return CommandType.C_OR
        if "not" in self.line:
            return CommandType.C_NOT
class CodeWriter:
    def __init__(self, file_output_name:str):
        self.file = open(file_output_name,'w')
        self.counter = 1
        self.current_file_name = file_output_name.split('/')[-1].split('.')[0]

    def load_base(self) -> None:
        # Initialize SP to 256
        self.file.write("@256\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")
        # Initialize LCL to 300
        self.file.write("@300\n")
        self.file.write("D=A\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")
        # Initialize ARG to 400
        self.file.write("@400\n")
        self.file.write("D=A\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")
        # Initialize THIS to 3000
        self.file.write("@3000\n")
        self.file.write("D=A\n")
        self.file.write("@THIS\n")
        self.file.write("M=D\n")
        # Initialize THAT to 3010
        self.file.write("@3010\n")
        self.file.write("D=A\n")
        self.file.write("@THAT\n")
        self.file.write("M=D\n")

    def get_segment(self, command_line: str) -> str:
        parts = command_line.split()
        if len(parts) >= 2:
            return parts[1]
        return ""

    def get_index(self, command_line: str) -> int:
        parts = command_line.split()
        if len(parts) >= 3:
            return int(parts[2])
        return 0

    def write_push_command(self, segment: str, index: int) -> None:
        file = self.file
        if segment == "argument":
            file.write(f"// push argument {index}\n")
            file.write(f"@{index}\n")
            file.write("D=A\n")
            file.write("@ARG\n")
            file.write("A=D+M\n")
            file.write("D=M\n")
            file.write("@SP\n")
            file.write("A=M\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("M=M+1\n")
        elif segment == "local":
            file.write(f"// push local {index}\n")
            file.write(f"@{index}\n")
            file.write("D=A\n")
            file.write("@LCL\n")
            file.write("A=D+M\n")
            file.write("D=M\n")
            file.write("@SP\n")
            file.write("A=M\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("M=M+1\n")
        elif segment == "static":
            file.write(f"// push static {index}\n")
            file.write(f"@{self.current_file_name}.{index}\n")
            file.write("D=M\n")
            file.write("@SP\n")
            file.write("A=M\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("M=M+1\n")
        elif segment == "constant":
            file.write(f"// push constant {index}\n")
            file.write(f"@{index}\n")
            file.write("D=A\n")
            file.write("@SP\n")
            file.write("A=M\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("M=M+1\n")
        elif segment == "this":
            file.write(f"// push this {index}\n")
            file.write(f"@{index}\n")
            file.write("D=A\n")
            file.write("@THIS\n")
            file.write("A=D+M\n")
            file.write("D=M\n")
            file.write("@SP\n")
            file.write("A=M\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("M=M+1\n")
        elif segment == "that":
            file.write(f"// push that {index}\n")
            file.write(f"@{index}\n")
            file.write("D=A\n")
            file.write("@THAT\n")
            file.write("A=D+M\n")
            file.write("D=M\n")
            file.write("@SP\n")
            file.write("A=M\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("M=M+1\n")
        elif segment == "pointer":
            file.write(f"// push pointer {index}\n")
            if index == 0:
                file.write("@THIS\n")
            elif index == 1:
                file.write("@THAT\n")
            file.write("D=M\n")
            file.write("@SP\n")
            file.write("A=M\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("M=M+1\n")
        elif segment == "temp":
            file.write(f"// push temp {index}\n")
            file.write(f"@{5 + index}\n")
            file.write("D=M\n")
            file.write("@SP\n")
            file.write("A=M\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("M=M+1\n")

    def write_pop_command(self, segment: str, index: int) -> None:
        file = self.file
        if segment == "argument":
            file.write(f"// pop argument {index}\n")
            file.write(f"@{index}\n")
            file.write("D=A\n")
            file.write("@ARG\n")
            file.write("D=D+M\n")
            file.write("@R13\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("AM=M-1\n")
            file.write("D=M\n")
            file.write("@R13\n")
            file.write("A=M\n")
            file.write("M=D\n")
        elif segment == "local":
            file.write(f"// pop local {index}\n")
            file.write(f"@{index}\n")
            file.write("D=A\n")
            file.write("@LCL\n")
            file.write("D=D+M\n")
            file.write("@R13\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("AM=M-1\n")
            file.write("D=M\n")
            file.write("@R13\n")
            file.write("A=M\n")
            file.write("M=D\n")
        elif segment == "static":
            file.write(f"// pop static {index}\n")
            file.write("@SP\n")
            file.write("AM=M-1\n")
            file.write("D=M\n")
            file.write(f"@{self.current_file_name}.{index}\n")
            file.write("M=D\n")
        elif segment == "constant":
            raise Exception("Cannot pop a constant")
        elif segment == "this":
            file.write(f"// pop this {index}\n")
            file.write(f"@{index}\n")
            file.write("D=A\n")
            file.write("@THIS\n")
            file.write("D=D+M\n")
            file.write("@R13\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("AM=M-1\n")
            file.write("D=M\n")
            file.write("@R13\n")
            file.write("A=M\n")
            file.write("M=D\n")
        elif segment == "that":
            file.write(f"// pop that {index}\n")
            file.write(f"@{index}\n")
            file.write("D=A\n")
            file.write("@THAT\n")
            file.write("D=D+M\n")
            file.write("@R13\n")
            file.write("M=D\n")
            file.write("@SP\n")
            file.write("AM=M-1\n")
            file.write("D=M\n")
            file.write("@R13\n")
            file.write("A=M\n")
            file.write("M=D\n")
        elif segment == "pointer":
            file.write(f"// pop pointer {index}\n")
            file.write("@SP\n")
            file.write("AM=M-1\n")
            file.write("D=M\n")
            if index == 0:
                file.write("@THIS\n")
            elif index == 1:
                file.write("@THAT\n")
            file.write("M=D\n")
        elif segment == "temp":
            file.write(f"// pop temp {index}\n")
            file.write("@SP\n")
            file.write("AM=M-1\n")
            file.write("D=M\n")
            file.write(f"@{5 + index}\n")
            file.write("M=D\n")

    def write_command(self, commandType: CommandType, command_line: str) -> None:
        file = self.file
        if commandType == CommandType.C_PUSH:
            segment = self.get_segment(command_line)
            index = self.get_index(command_line)
            self.write_push_command(segment, index)
        elif commandType == CommandType.C_POP:
            segment = self.get_segment(command_line)
            index = self.get_index(command_line)
            self.write_pop_command(segment, index)
        elif commandType == CommandType.C_ADD:
                file.write("//Add command\n")
                file.write("@SP\n")
                file.write("AM=M-1\n")
                file.write("D=M\n")
                file.write("A=A-1\n")
                file.write("M=D+M\n")
        elif commandType == CommandType.C_SUB:
                file.write("// sub\n")
                file.write("@SP\n")
                file.write("AM=M-1\n")
                file.write("D=M\n")
                file.write("A=A-1\n")
                file.write("M=M-D\n")
        elif commandType == CommandType.C_NEG:
                file.write("// neg\n")
                file.write("@SP\n")
                file.write("A=M-1\n")
                file.write("M=-M\n")
        elif commandType == CommandType.C_EQ:
                file.write("// eq\n")
                file.write("@SP\n")
                file.write("AM=M-1\n")
                file.write("D=M\n")
                file.write("A=A-1\n")
                file.write("D=M-D\n")
                file.write(f"@EQ_TRUE{self.counter}\n")
                file.write("D;JEQ\n")
                file.write("@SP\n")
                file.write("A=M-1\n")
                file.write("M=0\n")
                file.write(f"@EQ_END{self.counter}\n")
                file.write("0;JMP\n")
                file.write(f"(EQ_TRUE{self.counter})\n")
                file.write("@SP\n")
                file.write("A=M-1\n")
                file.write("M=-1\n")
                file.write(f"(EQ_END{self.counter})\n")
                self.counter += 1
        elif commandType == CommandType.C_GT:
                file.write("// gt\n")
                file.write("@SP\n")
                file.write("AM=M-1\n")
                file.write("D=M\n")
                file.write("A=A-1\n")
                file.write("D=M-D\n")
                file.write(f"@GT_TRUE{self.counter}\n")
                file.write("D;JGT\n")
                file.write("@SP\n")
                file.write("A=M-1\n")
                file.write("M=0\n")
                file.write(f"@GT_END{self.counter}\n")
                file.write("0;JMP\n")
                file.write(f"(GT_TRUE{self.counter})\n")
                file.write("@SP\n")
                file.write("A=M-1\n")
                file.write("M=-1\n")
                file.write(f"(GT_END{self.counter})\n")
                self.counter += 1
        elif commandType == CommandType.C_LT:
                file.write("// lt\n")
                file.write("@SP\n")
                file.write("AM=M-1\n")
                file.write("D=M\n")
                file.write("A=A-1\n")
                file.write("D=M-D\n")
                file.write(f"@LT_TRUE{self.counter}\n")
                file.write("D;JLT\n")
                file.write("@SP\n")
                file.write("A=M-1\n")
                file.write("M=0\n")
                file.write(f"@LT_END{self.counter}\n")
                file.write("0;JMP\n")
                file.write(f"(LT_TRUE{self.counter})\n")
                file.write("@SP\n")
                file.write("A=M-1\n")
                file.write("M=-1\n")
                file.write(f"(LT_END{self.counter})\n")
                self.counter += 1
        elif commandType == CommandType.C_AND:
                file.write("// and\n")
                file.write("@SP\n")
                file.write("AM=M-1\n")
                file.write("D=M\n")
                file.write("A=A-1\n")
                file.write("M=D&M\n")
        elif commandType == CommandType.C_OR:
                file.write("// or\n")
                file.write("@SP\n")
                file.write("AM=M-1\n")
                file.write("D=M\n")
                file.write("A=A-1\n")
                file.write("M=D|M\n")
        elif commandType == CommandType.C_NOT:
                file.write("// not\n")
                file.write("@SP\n")
                file.write("A=M-1\n")
                file.write("M=!M\n")
        
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