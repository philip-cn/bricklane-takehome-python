from decimal import Decimal
from dateutil.parser import parse


from bricklane_platform.models.card import Card
from bricklane_platform.models.bank import Bank

from bricklane_platform.config import PAYMENT_FEE_RATE


class Payment(object):

    customer_id = None
    date = None
    amount = None
    fee = None
    card_id = None
    bank_account_id = None
    source = None

    def __init__(self, data=None):

        if not data:
            return

        self.customer_id = int(data["customer_id"])
        self.date = parse(data["date"])

        total_amount = Decimal(data["amount"])
        self.fee = total_amount * PAYMENT_FEE_RATE
        self.amount = total_amount - self.fee

        if data.get("source") == "bank":
            bank = Bank()
            bank.bank_account_id = int(data["bank_account_id"])
            bank.status = data["bank_status"]
            self.bank = bank
            self.source = "bank"
        else:
            self.source = "card"
            card = Card()
            card.card_id = int(data["card_id"])
            card.status = data["card_status"]
            self.card = card

    def is_successful(self):
        if self.source == "bank":
            return self.bank.status == "processed"
        else:
            return self.card.status == "processed"
