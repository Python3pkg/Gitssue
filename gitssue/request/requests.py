"""
Concrete implementation requests_interface, using "requests" module.
"""
from request.request_interface import RequestInterface
import requests
import json


class Requests(RequestInterface):

    def get_request(self, request):
        """
        Executes a GET request.

        :param request: the GET request to execute.
        :return: response JSON object; False if the HTTP status code distinct to 200.
        """
        response = requests.get(request)
        response_object = json.loads(response.text)
        response.close()

        return response_object