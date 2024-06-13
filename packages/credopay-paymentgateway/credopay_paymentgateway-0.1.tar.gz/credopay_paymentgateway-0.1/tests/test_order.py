import unittest
from app.gateway import CredoPayPaymentGateway

class TestOrderAPI(unittest.TestCase):
    def setUp(self):
        self.gateway = CredoPayPaymentGateway('test_client_id', 'test_client_secret')
        self.order_api = self.gateway.order

    def test_create_order(self):
        order_data = {
            'receiptId': 'RE_DVGSD24535SFGER01',
            'amount': 1,
            'currency': 'INR',
            'description': 'Test Payment',
            'customerFields': {
                'name': 'Madhan R',
                'email': 'madhan.k@credopay.in',
                'phone': '1234567890'
            },
            'uiMode': 'checkout'
        }
        response = self.order_api.create_order(order_data)
        self.assertIn('resCode', response)

    def test_check_status(self):
        response = self.order_api.check_status('invalid_order_id')
        self.assertIn('resCode', response)

if __name__ == '__main__':
    unittest.main()
