
LINE_LENGTH = 16

destitaion_table = {
    'M': '001',
    'D': '010',
    'DM': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'ADM': '111'
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
def translate_asm(file_name: str):
    dot_file = file_name.find('.')
    name_file = file_name[0:dot_file]
    with open(f'{name_file}.asm', 'r') as file_input, open(f'{name_file}.out', 'w') as output_file:
        line = file_input.readline()
        while line:
            first_character = line[0]

            # A instruction
            if first_character == "@":
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

                destitation_bits = destitaion_table[line[:equal_sign_place]]

                jump_bits = '000'
                if semicolon_place != -1:
                    jump_bits = jump_table[line[:semicolon_place]]


                output_string += A_bit + comparator_bits + destitation_bits + jump_bits + '\n'
                output_file.write(output_string)


            line = file_input.readline()

if __name__ == '__main__':
    translate_asm('add.asm')