import io
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
import sys
import requests
from requests.auth import HTTPBasicAuth
import concurrent.futures
import keyring
from loguru import logger
from .spss_syntax.generate_labels import generate_labels_file
from .spss_syntax.generate_dataset import generate_dataset_file
from .spss_syntax.generate_open_all import generate_open_all_syntax
from .validate_inputs.validate_orgid import valid_orgid
from .validate_inputs.validate_surveyids import valid_surveyids
from .validate_inputs.validate_credentials import valid_credentials
from .validate_inputs.validate_output_path import valid_output_path

@dataclass
class DownloadSXData:
    """Funktion der henter data via SXs REST api fra en eller flere surveys.
    Funktionen antager at brugernavn og password for brugeren er gemt i windows credentials manager.
    output_path: str Sti hvor filerne skal gemmes
    survey_ids: int | list[int] | None Surveyid for den survey som du ønsker at downloade data for. Kan være en liste af surveys - ex. [1, 2, 3]. Kan udelades men kræver at org er angivet
    org_id: int Hvis du ønsker at downloade samtlige surveys i en org (ex. Results rum) så kan dette parameter anvendes. Default er None.
    cred_name: str Navnet på det sæt af credentials, som du ønsker at bruge til at få adgang til SX. Default er SXRest."""
    output_path: str
    survey_ids: int | list[int] = None
    org_id: int = None
    cred_name: str = 'SXRest'
    
    def __post_init__(self):
        self.__check_inputs()
        self.__org_download: bool = False
        if self.org_id:
            self.__org_download: bool = True
        self.__surveys = self.__parse_surveyids_orgid()
        
    def __check_inputs(self):
        validators = [
            (valid_output_path, self.output_path),
            (valid_surveyids, self.survey_ids),
            (valid_orgid, self.org_id),
            (valid_credentials, self.cred_name)
        ]
        for valid_func, arg in validators:
            if not valid_func(arg):
                sys.exit(0)
        
        if not self.survey_ids and not self.org_id:
            logger.error('Du skal enten angive surveyid eller org_id')
            sys.exit(0)
                
    def __parse_surveyids_orgid(self) -> list[int]:
        if self.__org_download:
            return self.__get_surveys_in_org()
        if isinstance(self.survey_ids, int):
            return [self.survey_ids]
        return self.survey_ids

    def download_data(self, spss: bool = False, fail_safe: bool = True) -> None:
        """Funktion som starter download.
        spss: bool Hvis denne sættes til true, så dannes der SPSS syntaxer. Default er false
        fail_safe: bool Hvis download fra mere 20 surveys igangsættes, så stopper funktioner med mindre dette parameter er sat til False. Dette for at beskytte imod noget helt vanvittigt."""
        if fail_safe and len(self.__surveys)>20:
            logger.warning(f'Du prøver at downloade data fra {len(self.__surveys)} surveys. Hvis dette er bevidst, så sæt fail_safe=False og kør funktionen igen.')
            return
        self.__downloaded_surveys: list[int] = self.__surveys
        # 
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            for _ in executor.map(self.__download_dataset,self.__surveys):
                pass
               
        if spss and self.__downloaded_surveys:
            self.__generate_spss_syntaxes()

    def __call_sx_api(self, url: str) -> requests.Response:
        try:
            response = requests.get(url, auth=HTTPBasicAuth(keyring.get_credential(self.cred_name, None).username, keyring.get_credential(self.cred_name, None).password))
            response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
            return response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                logger.error(f'Du synes ikke at have adgang til den kaldte ressource - {url} - {e}')
            else:
                logger.error(f'Der opstod en fejl - {e}')
    
    def __get_surveys_in_org(self) -> list[int]:
        url = f'https://rest.survey-xact.dk/rest/organizations/{self.org_id}/surveys'
        sx_output = self.__call_sx_api(url)
        xml_data = io.BytesIO(sx_output.content)
        xml_root = ET.parse(xml_data).getroot()
        surveys = xml_root.findall('survey')
        # logger.info(f'Data for sx organisation med id {self.org_id}')
        return [int(survey.find('id').text) for survey in surveys]
  
    def __download_dataset(self, surveyid: int) -> None:
        url = f'https://rest.survey-xact.dk/rest/surveys/{surveyid}/export/dataset?format=EU'
        sx_output = self.__call_sx_api(url)
        if not sx_output:
            self.__downloaded_surveys.remove(surveyid)
            return
        filename_full_path = Path(self.output_path, f'Dataset_{surveyid}.csv')
        with open(filename_full_path, 'wb') as output_file:
            output_file.write(sx_output.content)
        logger.info(f'Data fra surveyid {surveyid} downloaded og gemt i {filename_full_path}')

    def __generate_single_spss_syntax(self, survey: list[int]) -> None:
        labels = self.__download_labels(survey)
        variables = self.__download_variables(survey)
        labels_file = self.__convert_response_to_utf8_string(labels)
        variables_file = self.__convert_response_to_utf8_string(variables)
        generate_labels_file(survey, self.__syntax_folder, labels_file, variables_file)
        generate_dataset_file(survey, self.__syntax_folder, variables_file)
        logger.info(f'SPSS syntax for survey {survey} dannet.')

    def __generate_spss_syntaxes(self) -> None:
        logger.info('Starter med at generere SPSS syntaxer')
        self.__syntax_folder = Path(self.output_path, 'spss_syntax')
        self.__syntax_folder.mkdir(exist_ok=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            for _ in executor.map(self.__generate_single_spss_syntax, self.__downloaded_surveys):
                pass        
        generate_open_all_syntax(self.__downloaded_surveys, Path(self.output_path))
        logger.info(f'Færdig med at generere SPSS syntaxer. Er gemt i {self.__syntax_folder.as_posix()}')

    def __download_labels(self, surveyid: int) -> requests.Response:
        url = f'https://rest.survey-xact.dk/rest/surveys/{surveyid}/export/labels?format=EU'
        sx_output = self.__call_sx_api(url)
        if not sx_output:
            logger.error(f'Labels for {surveyid} kunne ikke downloades.')
        return sx_output

    def __download_variables(self, surveyid: int) -> requests.Response:
        url = f'https://rest.survey-xact.dk/rest/surveys/{surveyid}/export/variables?format=EU'
        sx_output = self.__call_sx_api(url)
        if not sx_output:
            logger.error(f'Variable for {surveyid} kunne ikke downloades.')
        return sx_output
        
    def __convert_response_to_utf8_string(self, response: requests.Response) -> str:
        response_file: io.BytesIO = io.BytesIO(response.content)
        response_file.seek(0)
        return response_file.getvalue().decode(encoding='ansi')


if __name__ == '__main__':
    test = DownloadSXData(
        output_path=r'C:\Users\ctf\pq_data\sx_test_rest',
        survey_ids=1636525,
        # org_id=331137
    )

    test.download_data(spss=True, fail_safe=False)