from flask import Flask, request, render_template, redirect, jsonify
import sqlite3
from datetime import datetime
from flask_cors import CORS

DB_FILE = 'wiki.db'
app = Flask(__name__)
CORS(app)

# ✅ 1. 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # 카테고리 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # 용어 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS terms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            content TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            author TEXT DEFAULT 'unknown',
            last_editor TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')

    # 기본 카테고리 추가
    categories = ['web', 'network', 'system', '기타']
    for cat in categories:
        c.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (cat,))
    
    conn.commit()
    conn.close()
    print("✅ 데이터베이스 초기화 완료")

# ✅ 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# ✅ 용어 추가 페이지
@app.route('/add')
def add_page():
    return render_template('add.html')

# ✅ 용어 추가 기능 (POST)
@app.route('/add_term', methods=['POST'])
def add_term():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    title = data.get('title')
    author = data.get('author')
    category_name = data.get('category')
    content = data.get('content')

    if not title or not author or not category_name or not content:
        return jsonify({'error': 'Missing required fields'}), 400

    # DB 저장 로직 ...

    return jsonify({'message': f"용어 '{title}'이(가) 추가되었습니다."}), 200

# ✅ 용어 삭제
def delete_term(title):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM terms WHERE title = ?', (title,))
    conn.commit()
    deleted = c.rowcount
    conn.close()
    return deleted > 0

# ✅ 용어 검색
def search_term(keyword):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT t.title, t.content, c.name, t.author, t.last_editor, t.created_at, t.updated_at
        FROM terms t
        JOIN categories c ON t.category_id = c.id
        WHERE LOWER(t.title) LIKE ? OR LOWER(t.content) LIKE ?
    ''', (f'%{keyword.lower()}%', f'%{keyword.lower()}%'))

    results = c.fetchall()
    conn.close()
    return results

# ✅ 앱 실행
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
