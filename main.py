from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('finance.db')
    return conn

# Эндпоинт для получения данных о выручке
@app.route('/_get_finance_plan_', methods=['GET'])
def get_finance_plan():
    # Получаем параметры start_date и end_date
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({'error': 'Both start_date and end_date are required'}), 400

    # Преобразуем строки дат в формат datetime
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format, expected YYYY-MM-DD'}), 400

    # Подключаемся к базе данных и выполняем запрос
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT date, revenue FROM finance_planfact
    WHERE date BETWEEN ? AND ?
    '''
    cursor.execute(query, (start_date, end_date))

    rows = cursor.fetchall()

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

    # Формируем результат
    result = [{'date': row[0], 'revenue': row[1]} for row in rows]

    return jsonify({'finance_planfact': result})

if __name__ == '__main__':
    app.run(debug=True)
