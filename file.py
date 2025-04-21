import logging

logging.basicConfig(filename="error.log", level=logging.ERROR)


def process_payment(amount):
    if amount is None:
        raise ValueError("Amount is None")
    if amount <= 0:
        raise ValueError("Amount must be positive")

    return True
