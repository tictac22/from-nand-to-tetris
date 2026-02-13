from compiler import Tokenizer, Compiler


files = [
        'ArrayTest/Main.jack',
        'ExpressionLessSquare/Main.jack',
]

for file in files:
    tokenizer = Tokenizer(file)

    while tokenizer.hasMoreTokens():
        tokenizer.advance()
    tokenizer.print_tokens(inConsole=False)

    parser = Compiler(tokenizer.tokens, file)
    parser.compile_class()
    parser.print_tokens()

    file_main = open(file.replace(".jack", ".xml"), 'r')
    file_main_content = file_main.readlines()
    file_main.close()
    
    file_output = open("parsing_tests/" + parser.file_name + "T_output.xml", 'r')
    file_output_content = file_output.readlines()
    file_output.close()
    
    for i in range(len(file_main_content)):
        file_main_line = file_main_content[i]
        file_output_line = file_output_content[i]
        normalized_main = ''.join(file_main_line.split())
        normalized_output = ''.join(file_output_line.split())
        assert normalized_main == normalized_output, (
            f"Line {i + 1} doesn't match after stripping spaces. File: {file}\n"
            f"Expected: {file_main_line}\n"
            f"Actual: {file_output_line}"
        )
    print("Files are equal!!!")
