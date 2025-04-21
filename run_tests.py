import unittest
from html_test_runner import HTMLTestRunner


loader = unittest.TestLoader()
suite = loader.discover(".", pattern="test_integration.py")


runner = HTMLTestRunner(output_file="report.html", title="Museum Test Report")
runner.run(suite)
