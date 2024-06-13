import base64
import platform
import requests
from .resources.order import OrderAPI
from .resources.transaction import TransactionAPI

class CredoPayPaymentGateway:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self._get_basic_auth_header(),
            'System-Name': platform.system(),
            'Node-Name': platform.node(),
            'Release': platform.release(),
            'Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor()
        })
        self.orders = OrderAPI(self.session)
        self.transactions = TransactionAPI(self.session)

    def _get_basic_auth_header(self):
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return f"Basic {encoded_credentials}"

    def _handle_request(self, method, url, **kwargs):
        try:
            response = method(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
