import yookassa
from yookassa import Payment
import uuid
from config import ACCOUNT_ID, SECRET_KEY

yookassa.Configuration.account_id = ACCOUNT_ID
yookassa.Configuration.secret_key = SECRET_KEY


def create(amount, chat_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            'value': amount,
            'currency': "RUB"
        },
        'paymnet_method_data': {
            'type': 'bank_card'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': 'https://t.me/your_bot'
        },
        'capture': True,
        'metadata': {
            'chat_id': chat_id
        },
        'description': 'Описание товара....'
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id


def check(payment_id):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        return payment.metadata
    else:
        return False