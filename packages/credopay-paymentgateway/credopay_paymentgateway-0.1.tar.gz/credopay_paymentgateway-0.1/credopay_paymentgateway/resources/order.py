from ..config import CREATE_ORDER_URL, CHECK_STATUS_URL

class OrderAPI:
    def __init__(self, session):
        self.session = session

    def create_order(self, order_data):
        return self.session.post(CREATE_ORDER_URL, json=order_data).json()

    def check_status(self, order_id):
        url = f"{CHECK_STATUS_URL}?orderId={order_id}"
        return self.session.get(url).json()
