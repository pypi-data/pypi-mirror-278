import codecs
from pathlib import Path

def generate_open_data_syntax(surveys: list[int], output_path: Path) -> str:
    spss_syntax = '\n'
    for survey in surveys:
        spss_syntax += f'* Opening dataset fra survey: {survey}\n\n'
        spss_syntax += 'GET\n'
        spss_syntax += f'FILE=\'{Path(output_path.parent, f'Dataset_{survey}.sav').as_posix()}\' .\n'
        spss_syntax += f'DATASET NAME Dataset_{survey} WINDOW=FRONT .\n\n'
    return spss_syntax
        
def generate_open_all_syntax(surveyids: list[int], output_path: Path) -> None:
    template = Path(Path(__file__).parent.resolve(), r'templates/generate_spss_datafiles.txt')
    with codecs.open(template, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    modified_content = template_content.replace('[WORK_PATH]', output_path.as_posix())
    full_file_name = Path(output_path, '1_Open_all_datasets.sps')
    
    modified_content += generate_open_data_syntax(surveyids, output_path)

    with codecs.open(full_file_name, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)