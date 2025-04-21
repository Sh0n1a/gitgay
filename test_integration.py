import unittest
from unittest.mock import patch
from handler import handle_payment_and_notify


class TestIntegration(unittest.TestCase):

    @patch("handler.send_notification")
    def test_successful_payment(self, mock_notify):
        self.assertTrue(handle_payment_and_notify(100))
        mock_notify.assert_called_once()

    def test_zero_amount(self):
        with self.assertRaises(ValueError):
            handle_payment_and_notify(0)

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            handle_payment_and_notify(-50)

    def test_none_amount(self):
        with self.assertRaises(ValueError):
            handle_payment_and_notify(None)


@patch("handler.send_notification")
@patch("file.process_payment", side_effect=Exception("DB error"))
def test_logging_on_exception(self, mock_process_payment, mock_send_notification):

    with self.assertRaises(Exception):
        handle_payment_and_notify(100)

    try:
        with open("error.log", "r", encoding="utf-8") as f:
            log_content = f.read()
            self.assertIn("Ошибка при обработке платежа", log_content)
    except FileNotFoundError:
        self.fail("Файл error.log не найден")


if __name__ == "__main__":
    unittest.main(True)
