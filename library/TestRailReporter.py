from typing import Dict
from library.ConfigLoader import ConfigLoader

import base64
import json
import requests
import os


class TestRailAPIClient:
    def __init__(self, base_url: str) -> None:
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'

    def send_get(self, uri: str, filepath: str = None) -> Dict:
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('GET', uri, filepath)

    def send_post(self, uri: str, data: dict) -> Dict:
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data) -> Dict:
        url = self.__url + uri

        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        if method == 'POST':
            if uri[:14] == 'add_attachment':    # add_attachment API method
                files = {'attachment': (open(data, 'rb'))}
                response = requests.post(url, headers=headers, files=files)
                files['attachment'].close()
            else:
                headers['Content-Type'] = 'application/json'
                payload = bytes(json.dumps(data), 'utf-8')
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except:     # response.content not formatted as JSON
                error = str(response.content)
            raise APIError('TestRail API returned HTTP %s (%s)' %
                           (response.status_code, error))
        else:
            if uri[:15] == 'get_attachment/':   # Expecting file, not JSON
                try:
                    open(data, 'wb').write(response.content)
                    return (data)
                except:
                    return ("Error saving attachment.")
            else:
                try:
                    return response.json()
                except:  # Nothing to return
                    return {}


class APIError(Exception):
    pass


class TestRailReporter:
    def __init__(self) -> None:
        config = ConfigLoader(os.path.dirname(
            __file__) + "\\..\\config", "global").config
        self.client = TestRailAPIClient(config['testrail']['server'])
        self.client.user = config['testrail']['user']
        self.client.password = config['testrail']['password']

    def add_result_for_case(
        self,
        test_run_id: str,
        test_case_id: str,
        status: str,
        comment: str,
    ) -> Dict:
        test_run_id = str(test_run_id)
        test_case_id = str(test_case_id)
        if status == 'PASS':
            status_id = 1
        elif status == 'FAIL':
            status_id = 5

        action = f"add_result_for_case/{test_run_id}/{test_case_id}"
        data = {
            'status_id': status_id,
            'comment': comment,
        }

        return self.client.send_post(action, data)
