import datetime
import os
from html import escape
import unittest

class HTMLTestRunner:
    def __init__(self, output_file="rep.html", title="Test Report"):
        self.output_file = output_file
        self.title = title

    def run(self, test_suite):
        result = unittest.TestResult()
        test_suite.run(result)

        timestamp = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        total = result.testsRun
        passed = total - len(result.failures) - len(result.errors)
        failed = len(result.failures)
        errors = len(result.errors)

        rows = ""
        for test, reason in result.failures + result.errors:
            rows += f"<tr><td>{escape(str(test))}</td><td>{escape(reason)}</td></tr>"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{self.title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; }}
                th {{ background-color: #f2f2f2; }}
                .summary {{ margin-top: 20px; }}
                .pass {{ color: green; }}
                .fail {{ color: red; }}
            </style>
        </head>
        <body>
            <h1>{self.title}</h1>
            <p>Generated: {timestamp}</p>
            <div class="summary">
                <p><strong>Total:</strong> {total}</p>
                <p class="pass"><strong>Passed:</strong> {passed}</p>
                <p class="fail"><strong>Failed:</strong> {failed}</p>
                <p class="fail"><strong>Errors:</strong> {errors}</p>
            </div>
            <table>
                <tr><th>Test</th><th>Reason</th></tr>
                {rows or "<tr><td colspan='2'>All tests passed.</td></tr>"}
            </table>
        </body>
        </html>
        """

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✔ Отчёт сгенерирован: {os.path.abspath(self.output_file)}")
