import os
import re

from compiler import Compiler2, Tokenizer


def normalize_label_style(line: str) -> str:
    # Treat `Main_0_IF_TRUE` and `Main.IF_TRUE.0` as equivalent.
    match = re.match(
        r'^(label|if-goto|goto)\s+([A-Za-z_][A-Za-z0-9_]*)_(\d+)_(IF_TRUE|IF_FALSE|IF_END|WHILE_EXP|WHILE_END)$',
        line.strip(),
    )
    if not match:
        return line
    cmd, class_name, index, label_type = match.groups()
    return f'{cmd} {class_name}.{label_type}.{index}'


def normalize_line(line: str) -> str:
    line = normalize_label_style(line)
    return ''.join(line.split())


jack_files = []
for root, _, files in os.walk('11'):
    for file_name in files:
        if file_name.endswith('.jack'):
            jack_files.append(os.path.join(root, file_name))

jack_files.sort()

for jack_file in jack_files:
    tokenizer = Tokenizer(jack_file)
    while tokenizer.hasMoreTokens():
        tokenizer.advance()

    parser = Compiler2(tokenizer.tokens, jack_file)
    parser.compile_class()

    expected_vm_path = jack_file.replace('.jack', '.vm')
    assert os.path.exists(expected_vm_path), (
        f"Expected VM file not found for comparison: {expected_vm_path}"
    )

    expected_lines = open(expected_vm_path, 'r').readlines()
    actual_lines = parser.vmWriter.output.splitlines()

    assert len(actual_lines) == len(expected_lines), (
        f"Line count mismatch for {jack_file}\n"
        f"Expected: {len(expected_lines)} lines\n"
        f"Actual: {len(actual_lines)} lines"
    )

    for i, expected_line in enumerate(expected_lines):
        actual_line = actual_lines[i]
        normalized_expected = normalize_line(expected_line)
        normalized_actual = normalize_line(actual_line)
        assert normalized_actual == normalized_expected, (
            f"Mismatch in file {jack_file} at line {i + 1}\n"
            f"Expected: {expected_line.rstrip()}\n"
            f"Actual: {actual_line.rstrip()}"
        )

    print(f"Files are equal: {jack_file}")
