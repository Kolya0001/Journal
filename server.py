import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request, redirect

# Загружаем переменные из .env файла
load_dotenv()

app = Flask(__name__)

# Устанавливаем параметры подключения, используя переменные окружения
db_config = {
    'dbname': os.getenv('DB_NAME', 'sitedb'),        # Имя базы данных
    'user': os.getenv('DB_USER', 'admin'),           # Имя пользователя
    'password': os.getenv('DB_PASSWORD', ''),        # Пароль из переменной окружения
    'host': os.getenv('DB_HOST', ''),                # IP-адрес теперь из переменной окружения
    'port': int(os.getenv('DB_PORT', 5432))          # Порт
}

# Функция для подключения к базе данных
def get_db_connection():
    connection = psycopg2.connect(**db_config)
    return connection

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница для создания нового журнала записи
@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO journal_entries (title, content) VALUES (%s, %s)', (title, content))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/')
    return render_template('add_entry.html')

# Страница для редактирования записи
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        cursor.execute('UPDATE journal_entries SET title = %s, content = %s WHERE id = %s', (title, content, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/journal')

    cursor.execute('SELECT * FROM journal_entries WHERE id = %s', (id,))
    entry = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('edit_entry.html', entry=entry)

# Страница для просмотра всех записей
@app.route('/journal')
def journal():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM journal_entries ORDER BY created_at DESC')
    entries = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('journal.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
