import codecs
from pathlib import Path

def generate_variables_syntax(variables: str) -> str:
    variables_map = ''
    lines = variables.splitlines()
    for line in lines[1:]:
        components = line.strip().split(';')
        variable, label = components
        variables_map += f'  {variable.replace('"', '')} AUTO\n'
    return variables_map
    

def generate_dataset_file(surveyid: int, output_path: Path, variables: str) -> None:
    # Setting up parameters
    dataset_full_path = Path(output_path.parent, f'Dataset_{surveyid}.csv').as_posix()
    variable_syntax = generate_variables_syntax(variables)
    dataset_name = f'Dataset_{surveyid}'
    labels_full_path = Path(output_path, f'Labels_{surveyid}.sps').as_posix()
    dataset_spss_full_path = Path(output_path.parent, f'Dataset_{surveyid}.csv').as_posix()
    # Map som bruges til at erstatte placeholders i skabelonen
    replace_map = {
        '[DATASET_FULL_PATH]': dataset_full_path,
        '[VARIABLE_MAP]': variable_syntax,
        '[DATASET_NAME]': dataset_name,
        '[LABELS_FULL_PATH]': labels_full_path,
        '[DATASET_SPSS_FULL_PATH]': dataset_spss_full_path,
    }

    # Åbner skabelonfilen
    template = Path(Path(__file__).parent.resolve(), r'templates/open_single_dataset_in_spss.txt')
    with codecs.open(template, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    
    # Tilpasser skabelonen ved at erstatte placeholder via mappet
    modified_content = template_content
    for placeholder, replacement in replace_map.items():
        modified_content = modified_content.replace(placeholder, replacement)    

    full_file_name = Path(output_path, f'Generate_dataset_{surveyid}.sps')
    with codecs.open(full_file_name, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)
