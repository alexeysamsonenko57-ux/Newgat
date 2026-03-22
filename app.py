from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def get_neighbors(city):
    # Простая база соседей для теста
    neighbors_map = {
        "Ірпінь": ["Бучу", "Ворзель", "Гостомель"],
        "Київ": ["Бровари", "Вишгород", "Бориспіль"],
        "Одеса": ["Чорноморськ", "Южне", "Затока"]
    }
    return neighbors_map.get(city, ["сусідніх селищ", "вашого району", "області"])

@app.route('/')
def index():
    # Определяем город по IP
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    try:
        # Бесплатный API для определения локации
        response = requests.get(f"http://ip-api.com/json/{user_ip}?lang=uk").json()
        city = response.get('city', 'Київ')
    except:
        city = "Київ"

    neighbors = get_neighbors(city)
    headline = f"ТІЛЬКИ ДЛЯ МЕШКАНЦІВ {city.upper()}, {', '.join(neighbors).upper()} ТА ОКОЛИЦЬ"

    # Динамический текст под время (вечер воскресенья!)
    now = datetime.now()
    status = f"Доступ підтверджено. Сьогодні {now.strftime('%d.%m.%Y')}. Реєстрація активна ще 14 хвилин."

    return render_template('index.html', headline=headline, city=city, status=status)

if __name__ == "__main__":
    app.run()
  
