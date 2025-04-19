import logging
import unittest
from unittest.mock import patch
import os
import __main__  # для корректного мока в одном файле

# === НАСТРОЙКА ЛОГГИРОВАНИЯ ===
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === ФУНКЦИЯ ===
def factorial(n):
    if not isinstance(n, int):
        logging.error("ValueError: Input must be an integer")
        raise ValueError("Input must be an integer")
    if n < 0:
        logging.error("ValueError: Input must be a non-negative integer")
        raise ValueError("Input must be a non-negative integer")

    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# === ТЕСТЫ ===
class TestFactorial(unittest.TestCase):

    def setUp(self):
        try:
            if os.path.exists('error.log'):
                os.remove('error.log')
        except Exception as e:
            print(f"Не удалось удалить error.log: {e}")



    def test_factorial_valid(self):
        self.assertEqual(factorial(5), 120)

    def test_factorial_zero(self):
        self.assertEqual(factorial(0), 1)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_factorial_non_integer(self):
        with self.assertRaises(ValueError):
            factorial("abc")

    def test_factorial_logging_error_message(self):
        try:
            factorial(-10)
        except ValueError:
            pass

        # Проверка существования лог-файла
        self.assertTrue(os.path.exists("error.log"))

        # Проверка содержания лог-файла
        with open("error.log", "r", encoding="utf-8") as f:
            log_content = f.read()
            self.assertIn("Input must be a non-negative integer", log_content)

    def test_logging_mock(self):
        # ⚠️ ВНИМАНИЕ: мокать нужно путь к функции, как она используется в __main__
        with patch.object(__main__.logging, 'error') as mock_log:
            with self.assertRaises(ValueError):
                factorial(-5)
            mock_log.assert_called_with("ValueError: Input must be a non-negative integer")


# === ЗАПУСК ===
if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)
