import string
from json import dumps
from typing import Optional, List, Iterator

import requests
from gensim.parsing.preprocessing import strip_tags
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document

PAGE_NUMBER = 1


class AnalystaQTestApiDataLoader(BaseLoader):

    def __init__(self,
                 project_id: int,
                 no_of_test_cases_per_page: int,
                 qtest_api_token: str,
                 qtest_api_base_url: str,
                 module_id: Optional[int] = None,
                 columns: Optional[List[str]] = None
                 ):
        self.project_id = project_id
        self.no_of_test_cases_per_page = no_of_test_cases_per_page
        self.qtest_api_token = qtest_api_token
        self.qtest_api_base_url = qtest_api_base_url
        self.module_id = module_id
        self.columns = columns

    def __prepare_request_endpoint(self, page_number: Optional[int] = None) -> tuple[str, dict]:
        url_str: str = f'{self.qtest_api_base_url}/projects/{self.project_id}/test-cases'
        params = {
            'size': self.no_of_test_cases_per_page,
            'expandSteps': 'true'
        }

        if page_number is None:
            params['page'] = PAGE_NUMBER
        else:
            params['page'] = page_number

        if self.module_id is not None:
            params['parentId'] = self.module_id
        return url_str, params

    def __fetch_test_cases_from_qtest_as_data_frame(self) -> list:
        request_headers: dict = {'Authorization': f"{self.qtest_api_token}", 'content_type': 'application/json'}
        no_of_test_cases_returned_by_api_per_page = self.no_of_test_cases_per_page
        no_of_pages_counter = PAGE_NUMBER

        test_cases_list: list = []

        while no_of_test_cases_returned_by_api_per_page == self.no_of_test_cases_per_page:
            url, params = self.__prepare_request_endpoint(no_of_pages_counter)
            json_response = requests.get(url=url, params=params,
                                         headers=request_headers).json()

            no_of_test_cases_returned_by_api_per_page = len(json_response)
            if no_of_test_cases_returned_by_api_per_page < 1:
                break

            temp_list: list = self.__transform_test_data_into_dict(json_response)
            test_cases_list += temp_list
            no_of_pages_counter += 1

        return test_cases_list

    @staticmethod
    def __transform_test_data_into_dict(json_response: list) -> list:
        import html
        fields_to_pick_from_api_response: list = ['name', 'pid', 'description', 'precondition', 'test_steps']
        result: list = []

        for json_response_current_object in json_response:
            api_data_dict: dict = {}
            for key_name in json_response_current_object:
                current_key_data = json_response_current_object[key_name]
                if key_name in fields_to_pick_from_api_response:
                    if key_name == 'test_steps':
                        api_data_dict['Test Step Description'] = '\n'.join(map(str,
                                                                               [html.unescape(str(
                                                                                   item['order']) + '. ' + strip_tags(
                                                                                   item['description']))
                                                                                for item in current_key_data
                                                                                for key in item
                                                                                if key == 'description']))
                        api_data_dict['Test Expected Result'] = '\n'.join(map(str,
                                                                              [html.unescape(str(
                                                                                  item['order']) + '. ' + strip_tags(
                                                                                  item['expected']))
                                                                               for item in
                                                                               current_key_data
                                                                               for key in item
                                                                               if
                                                                               key == 'expected']))
                    else:
                        if key_name == "description" or key_name == "precondition":
                            filtered_data: str = strip_tags(current_key_data)
                            if api_data_dict.get(key_name) is None:
                                api_data_dict[string.capwords(key_name)] = html.unescape(filtered_data)
                            else:
                                if filtered_data not in api_data_dict[key_name]:
                                    api_data_dict[string.capwords(key_name)] = html.unescape(filtered_data)
                        elif key_name == "pid":
                            api_data_dict['Id'] = current_key_data
                        else:
                            api_data_dict[string.capwords(key_name)] = current_key_data
            result.append(api_data_dict)
        return result

    def load(self) -> List[Document]:
        documents: List[Document] = []
        qtest_data: list = self.__fetch_test_cases_from_qtest_as_data_frame()
        if self.columns:
            for row in qtest_data:
                # Merge specified content using a new line symbol
                page_content = '\n'.join([row[col] for col in self.columns])
                # Create metadata dictionary
                meta = {
                    'table_source': f'qTest project id - {self.project_id}',
                    'source': str(row['Id']),
                    'columns': list(row.keys()),
                    'og_data': dumps(row),
                }
                # Create Langchain document and add to the list
                documents.append(Document(page_content, metadata=meta))
        else:
            for row in qtest_data:
                # Merge specified content using a new line symbol
                page_content = '\n'.join([row[col] for col in row.keys()])
                # Create metadata dictionary
                meta = {
                    'table_source': f'qTest project id - {self.project_id}',
                    'source': str(row['Id']),
                    'columns': list(row.keys()),
                    'og_data': dumps(row),
                }
                # Create Langchain document and add to the list
                documents.append(Document(page_content, metadata=meta))
        return documents

    def lazy_load(self) -> Iterator[Document]:
        qtest_data: list = self.__fetch_test_cases_from_qtest_as_data_frame()
        if self.columns:
            for row in qtest_data:
                # Merge specified content using a new line symbol
                page_content = '\n'.join([row[col] for col in self.columns])
                # Create metadata dictionary
                meta = {
                    'table_source': f'qTest project id - {self.project_id}',
                    'source': str(row['Id']),
                    'columns': list(row.keys()),
                    'og_data': dumps(row),
                }
                # Create Langchain document and add to the list
                yield Document(page_content, metadata=meta)
        else:
            for row in qtest_data:
                # Merge specified content using a new line symbol
                page_content = '\n'.join([row[col] for col in row.keys()])
                # Create metadata dictionary
                meta = {
                    'table_source': f'qTest project id - {self.project_id}',
                    'source': str(row['Id']),
                    'columns': list(row.keys()),
                    'og_data': dumps(row),
                }
                # Create Langchain document and add to the list
                yield Document(page_content, metadata=meta)
