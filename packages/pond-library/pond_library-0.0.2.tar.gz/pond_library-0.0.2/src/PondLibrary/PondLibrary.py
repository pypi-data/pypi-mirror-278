import os
import json
import requests


class PondLibrary:
    def __init__(self, username, password) -> None:
        try:
            self.__agent_url = "http://154.91.170.22:30001"
            self.username = username
            self.password = password
            self.__token = self._get_token(self.username, self.password)
        except Exception as error:
            raise Exception(error)

    def __check_response(self, response):
        message = ""
        if int(response.status_code) == 500:
            message = "Internal Server Error"
        elif int(response.status_code) == 401:
            message = "Unauthorized"
        elif int(response.status_code) == 401:
            message = "Forbidden"
        elif int(response.status_code) == 200:
            message = "Success"
        else:
            message = "Error"
        return message

    def _get_token(self, username, password):
        payload = {}
        headers = {}
        ulr_with_parameters = f"{self.__agent_url}/user/get_token?username={username}&password={password}"
        response = requests.request(
            "GET", ulr_with_parameters, headers=headers, data=payload)
        result = self.__check_response(response)
        if result == "Success":
            response_data = json.loads(response.text)
            return response_data['token']
        else:
            raise Exception(result)

    def upload_file(self, domain_name, bucket_name, bucket_type, file_path):
        try:
            file_name = os.path.basename(file_path)
            ulr_with_parameters = f"{self.__agent_url}/datasource/upload_objects"
            payload = {
                'name': bucket_name,
                'type': bucket_type,
                'domain_name': domain_name,
            }
            files = [
                ('file', (
                    file_name,
                    open(file_path, 'rb'),
                    'application/json'
                ))
            ]
            headers = {
                'Authorization': f'Bearer {self.__token}'
            }

            response = requests.request(
                "POST", ulr_with_parameters, headers=headers, data=payload, files=files)
            result = self.__check_response(response)
            if result == "Success":
                print(response.text)
            else:
                raise Exception(result)
        except Exception as error:
            raise Exception(error)

    def download_file(self, domain_name, bucket_name, file_name):
        try:
            url = f"{self.__agent_url}/datasource/download_bucket_objects?name={bucket_name}&domain_name={domain_name}&object_name={file_name}"
            payload = {}
            headers = {
                'Authorization': f'Bearer {self.__token}'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            result = self.__check_response(response)
            if result == "Success":
                return response.content
            else:
                raise Exception(result)
        except Exception as error:
            raise Exception(error)
