import requests
import sqlite3
from config import ACCESS_TOKEN

# 1. Запрашиваем данные по API
api_url = "https://store-demo-test.ru/_get_finance_plan_"
params = {
    'start_date': '2024-01-01',
    'end_date': '2024-01-31'
}
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}
response = requests.get(api_url, params=params, headers=headers)

if response.status_code != 200:
    print(f"Ошибка при запросе данных: {response.status_code}")
    exit()

api_data = response.json()
finance_planfact = api_data.get('finance_planfact', [])

# 2. Создаем локальную базу данных и таблицу
conn = sqlite3.connect('finance.db')  # Это для SQLite, для другой БД возьмем из config.py
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS finance_planfact (
    date TEXT,
    revenue REAL
)
''')
conn.commit()

# 3. Сохраняем данные в базу данных
for record in finance_planfact:
    date = record['data']
    revenue = record['revenue']
    cursor.execute('INSERT INTO finance_planfact (date, revenue) VALUES (?, ?)', (date, revenue))
conn.commit()

print("Данные успешно сохранены в локальную базу данных.")

# 4. Проверяем сохраненные данные
cursor.execute('SELECT * FROM finance_planfact')
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
