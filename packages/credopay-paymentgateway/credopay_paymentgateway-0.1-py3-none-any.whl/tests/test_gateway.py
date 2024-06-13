import unittest
from app.gateway import CredoPayPaymentGateway

class TestCredoPayPaymentGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = CredoPayPaymentGateway('test_client_id', 'test_client_secret')

    def test_get_basic_auth_header(self):
        header = self.gateway._get_basic_auth_header()
        self.assertTrue(header.startswith("Basic "))

    def test_handle_request(self):
        response = self.gateway._handle_request(self.gateway.session.get, 'https://jsonplaceholder.typicode.com/todos/1')
        self.assertIn('title', response)

if __name__ == '__main__':
    unittest.main()
