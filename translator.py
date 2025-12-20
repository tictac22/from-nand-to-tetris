
LINE_LENGTH = 16

destitaion_table = {
    'M': '001',
    'D': '010',
    'DM': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'ADM': '111',
    'MD': '011'
}

jump_table = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '001',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

comparator_table = {
  "0":   "101010",
  "1":   "111111",
  "-1":  "111010",
  "D":   "001100",
  "A":   "110000",
  "!D":  "001101",
  "!A":  "110001",
  "-D":  "001111",
  "-A":  "110011",
  "D+1": "011111",
  "A+1": "110111",
  "D-1": "001110",
  "A-1": "110010",
  "D+A": "000010",
  "D-A": "010011",
  "A-D": "000111",
  "D&A": "000000",
  "D|A": "010101"
}

predifend_symbol_table = {
    'R0': '0',
    'R1': '1',
    'R2': '2',
    'R3': '3',
    'R4': '4',
    'R5': '5',
    'R6': '6',
    'R7': '7',
    'R8': '8',
    'R9': '9',
    'R10': '10',
    'R11': '11',
    'R12': '12',
    'R13': '13',
    'R14': '14',
    'R15': '15',
    'SCREEN': '16384',
    'KBD': '24576',
    'SP': '0',
    'LCL': '1',
    'ARG': '2',
    'THIS': '3',
    'THAT': '4'
}
line_counter = 0
def read_first_time(file_name: str) -> None:
    global line_counter
    line_counter = 0
    with open(file_name, 'r') as file_input:
        line = file_input.readline()
        while line:
            # skip comments or empty lines
            if '//' in line or len(line) == 1:
                line = file_input.readline()
                continue
            line = line.replace(" ", '').replace('\n','')
            first_character = line[0]
            if first_character == "(":
                closed_paretheses = line.find(')')
                symbol = line[1:closed_paretheses]
                predifend_symbol_table[symbol] = line_counter
                line = file_input.readline() 
                continue
            line = file_input.readline()
            line_counter += 1
                

symbols_counter = 16
def translate_asm(file_name: str):
    read_first_time(file_name)
    dot_file = file_name.find('.')
    global symbols_counter
    symbols_counter = 16
    name_file = file_name[0:dot_file]
    with open(f'{name_file}.asm', 'r') as file_input, open(f'{name_file}.out', 'w') as output_file:
        line = file_input.readline()
        while line:
            # skip comments or empty lines
            if '//' in line or len(line) == 1 or line[0] == '(':
                line = file_input.readline()
                continue

            line = line.replace(" ", '').replace('\n','')
            first_character = line[0]
            # A instruction
            if first_character == "@":
                # predefined symbol
                if line[1:] in predifend_symbol_table:
                    symbol = predifend_symbol_table[line[1:]]
                    binary_number = bin((int(symbol)))[2:]
                # variable symbols
                elif line[1:] not in predifend_symbol_table and str.isdigit(line[1:]) is False:
                    predifend_symbol_table[line[1:]] = symbols_counter
                    binary_number = bin(symbols_counter)[2:]
                    symbols_counter += 1
                # numbers
                else:
                    number = line[1:]
                    binary_number = bin((int(number)))[2:]

                output_string = '0'

                remaining_zeros = LINE_LENGTH - len(binary_number) - 1

                output_string += '0' * remaining_zeros + binary_number + '\n'
                output_file.write(output_string)
            # C instruciton
            else:
                # dest = comp ; jump
                # 1 1 1 a c c c c c c d d d j j j
                output_string = '111'
                equal_sign_place = line.find('=')
                semicolon_place = line.find(';')

                if semicolon_place == -1:
                    comparator_string = line[equal_sign_place +1:]
                    if comparator_string[-1] == '\n':
                        comparator_string = comparator_string[:-1]
                else:
                    comparator_string = line[equal_sign_place +1:semicolon_place]
                A_bit = '0'

                comparator_bits = ''

                if comparator_string in comparator_table:
                    comparator_bits = comparator_table[comparator_string]
                else:
                    comparator_bits = comparator_table[comparator_string.replace('M','A')]
                    A_bit = '1'

                if line[:equal_sign_place] in destitaion_table:
                    destitation_bits = destitaion_table[line[:equal_sign_place]]
                else:
                    destitation_bits = '000'

                jump_bits = '000'
                if semicolon_place != -1:
                    jump_bits = jump_table[line[semicolon_place+1:]]


                output_string += A_bit + comparator_bits + destitation_bits + jump_bits + '\n'
                output_file.write(output_string)


            line = file_input.readline()

if __name__ == '__main__':
    file_name = input("File Name: \n")
    translate_asm(file_name)
