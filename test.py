
FILES = [
    'add',
    'max',
    'maxL',
    'rect',
    'rectL',
    'pong',
    'pongL'
]


from translator import translate_asm

for FILE_NAME in FILES:
    print(f"Comparing {FILE_NAME}.asm")
    translate_asm(f'{FILE_NAME}.asm')
    with open(f'{FILE_NAME}.out', 'r') as file_output, open(f'{FILE_NAME}.test', 'r') as test_file:
        output_line = file_output.readline()
        test_line = test_file.readline()        
        while output_line:
            assert output_line == test_line, f"Line {output_line} doesn't equal with line {test_line}"
            test_line = test_file.readline()
            output_line = file_output.readline()
            if test_line.endswith('\n'):
                test_line = test_line[:-1]
            if output_line.endswith('\n'):
                output_line = output_line[:-1]
        print("Files are the same!!")
