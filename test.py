import logging
import unittest
from unittest.mock import patch
import os
import __main__
import sys

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
        self.assertTrue(os.path.exists("error.log"))
        with open("error.log", "r", encoding="utf-8") as f:
            log_content = f.read()
            self.assertIn("Input must be a non-negative integer", log_content)

    def test_logging_mock(self):
        with patch.object(__main__.logging, 'error') as mock_log:
            with self.assertRaises(ValueError):
                factorial(-5)
            mock_log.assert_called_with("ValueError: Input must be a non-negative integer")
def test_addition(self):
    print(">>> тест пошёл!")
    self.assertEqual(2 + 2, 4)


# === ЗАПУСК ===
if __name__ == "__main__":
    if "--web" in sys.argv:
        from flask import Flask, request, redirect, url_for, render_template_string

        app = Flask(__name__)
        lots = []  # Список лотов аукциона

        html_template = '''
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Аукцион Редких Вещей</title>
            <style>
                body { font-family: sans-serif; max-width: 800px; margin: auto; background: #f9f9f9; padding: 20px; }
                h1 { color: darkblue; }
                .lot { border: 1px solid #ccc; padding: 10px; margin: 10px 0; background: white; }
                form { margin-top: 20px; }
                label { display: block; margin-top: 10px; }
                input, textarea { width: 100%; padding: 5px; }
                button { margin-top: 10px; padding: 10px; background: darkblue; color: white; border: none; }
            </style>
        </head>
        <body>
            <h1>Аукцион Редких и Старинных Вещей</h1>

            <h2>Добавить Лот</h2>
            <form method="post" action="/">
                <label>Название:</label>
                <input type="text" name="name" required>
                <label>Описание:</label>
                <textarea name="description" required></textarea>
                <label>Стартовая цена (₽):</label>
                <input type="number" name="price" required>
                <button type="submit">Добавить лот</button>
            </form>

            <h2>Текущие Лоты</h2>
            {% if lots %}
                {% for lot in lots %}
                    <div class="lot">
                        <strong>{{ lot.name }}</strong> — {{ lot.price }} ₽<br>
                        <em>{{ lot.description }}</em>
                        <form method="post" action="/bid">
                            <input type="hidden" name="name" value="{{ lot.name }}">
                            <label>Новая ставка (₽):</label>
                            <input type="number" name="new_bid" required>
                            <button type="submit">Сделать ставку</button>
                        </form>
                    </div>
                {% endfor %}
            {% else %}
                <p>Пока нет лотов.</p>
            {% endif %}
        </body>
        </html>
        '''

        @app.route("/", methods=["GET", "POST"])
        def index():
            if request.method == "POST":
                try:
                    name = request.form["name"]
                    description = request.form["description"]
                    price = float(request.form["price"])
                    lots.append({"name": name, "description": description, "price": price})
                except Exception as e:
                    logging.error(f"Ошибка при добавлении лота: {e}")
            return render_template_string(html_template, lots=lots)

        @app.route("/bid", methods=["POST"])
        def bid():
            name = request.form["name"]
            try:
                new_bid = float(request.form["new_bid"])
                for lot in lots:
                    if lot["name"] == name and new_bid > lot["price"]:
                        lot["price"] = new_bid
                        break
            except Exception as e:
                logging.error(f"Ошибка при ставке: {e}")
            return redirect(url_for('index'))

        app.run(debug=True)
    else:
        unittest.main(verbosity=2, exit=False)
