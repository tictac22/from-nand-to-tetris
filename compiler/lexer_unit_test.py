
from compiler import Tokenizer


files = [
        'ArrayTest/Main.jack',
        'ExpressionLessSquare/Main.jack',
        'ExpressionLessSquare/Square.jack',
        'ExpressionLessSquare/SquareGame.jack',
        'Square/Main.jack',
        'Square/Square.jack',
        'Square/SquareGame.jack'
]
for file in files:
    tokenizer = Tokenizer(file)

    while tokenizer.hasMoreTokens():
        tokenizer.advance()
    tokenizer.print_tokens(inConsole=False)
    file_main = open(file.replace(".jack", "T.xml"), 'r')
    file_main_content = file_main.readlines()
    file_main.close()
    
    file_output = open("lexer_tests/" + tokenizer.file_name + "T_output.xml", 'r' )
    file_output_content = file_output.readlines()
    file_output.close()
    
    for i in range(len(file_main_content)):
        file_main_line = file_main_content[i]
        file_output_line = file_output_content[i]
        assert file_main_line == file_output_line, f"Line {file_main_line} doesn't equal with line {file_output_line}. File: {file}"
    print("Files are equal!!!")
