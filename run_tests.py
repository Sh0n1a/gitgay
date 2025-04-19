import unittest
from html_test_runner import HTMLTestRunner

# Загружаем тесты из test_integration.py
loader = unittest.TestLoader()
suite = loader.discover('.', pattern='test_integration.py')

# Создаём и запускаем HTML-репорт
runner = HTMLTestRunner(output_file="report.html", title="Museum Test Report")
runner.run(suite)
