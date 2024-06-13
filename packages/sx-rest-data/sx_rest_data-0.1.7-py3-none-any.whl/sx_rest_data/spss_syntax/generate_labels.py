import codecs
from pathlib import Path

def generate_labels_syntax(labels_file: str) -> str:
    spss_syntax = "* Variables and value labels .\n"
    lines = labels_file.splitlines()
    for line in lines:
        components = line.strip().split(';')
        variable, value, label = components
        spss_syntax += f'add value labels {variable.replace('"', '')} {value} \'{label.replace('"', '')}\' .\n'
    return spss_syntax

def generate_variables_syntax(variables_file: str) -> str:
    variables_syntax = ''
    lines = variables_file.splitlines()
    for line in lines[1:]:
        components = line.strip().split(';')
        variable, label = components
        variables_syntax += f'var lab {variable.replace('"', '')} \'{label.replace('"', '')}\' .\n'
    return variables_syntax

def generate_labels_file(surveyid: int, output_path: Path, labels: str, variables: str) -> None:
    full_file_name = Path(output_path, f'Label_{surveyid}.sps')
    labels_syntax = generate_labels_syntax(labels)
    variables_syntax = generate_variables_syntax(variables)
    full_syntax = f'{labels_syntax}\n\n{variables_syntax}'
    with codecs.open(full_file_name, 'w', encoding='utf-8') as output_file:
        output_file.write(full_syntax)

