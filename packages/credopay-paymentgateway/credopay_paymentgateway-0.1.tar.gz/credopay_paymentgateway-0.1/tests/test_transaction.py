import unittest
from app.gateway import CredoPayPaymentGateway

class TestTransactionAPI(unittest.TestCase):
    def setUp(self):
        self.gateway = CredoPayPaymentGateway('test_client_id', 'test_client_secret')
        self.transaction_api = self.gateway.transaction

    def test_transaction_api_initialization(self):
        self.assertIsNotNone(self.transaction_api)

if __name__ == '__main__':
    unittest.main()
