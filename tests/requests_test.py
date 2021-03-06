import unittest
from unittest import mock
from requests.exceptions import RequestException
from gitssue.request.requests import Requests
from gitssue.request.unsuccessful_http_request_exception import UnsuccessfulHttpRequestException


class RequestsTest(unittest.TestCase):

    def setUp(self):
        self.requests = Requests()

    @mock.patch('requests.get')
    def test_get_request(self, requests_get_mock):
        response_mock = mock.Mock()
        mocked_return = """
            {
                "field_1": "value_1",
                "field_2": "value_2"
            }
        """
        expected = {
            'field_1': 'value_1',
            'field_2': 'value_2',
        }

        attributes = {
            'status_code': 200,
            'text': mocked_return,
            'close.return_value': None,
        }
        response_mock.configure_mock(**attributes)
        requests_get_mock.return_value = response_mock

        actual = self.requests.get_request('some request')

        self.assertEqual(expected, actual)

    @mock.patch('requests.get')
    def test_get_request_status_not_200(self, requests_get_mock):
        response_mock = mock.Mock()

        attributes = {
            'status_code': 404,
            'headers': {'header_key': 'header_value'}
        }
        response_mock.configure_mock(**attributes)
        requests_get_mock.return_value = response_mock

        with self.assertRaises(UnsuccessfulHttpRequestException):
            self.requests.get_request('some request')

    @mock.patch('requests.get')
    def test_get_request_request_exception(self, requests_get_mock):
        requests_get_mock.side_effect = RequestException

        with self.assertRaises(RequestException):
            self.requests.get_request('some request')

