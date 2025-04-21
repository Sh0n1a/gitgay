from file import process_payment
from file2 import send_notification
import logging


def handle_payment_and_notify(amount):
    try:
        result = process_payment(amount)
        if result:
            send_notification(f"Платёж на сумму {amount} успешно обработан.")
        return result
    except Exception as e:
        logging.error(f"Ошибка при обработке платежа: {str(e)}")
        raise
