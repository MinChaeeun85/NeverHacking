import sqlite3
from datetime import datetime

DB_FILE = 'wiki.db'

# ✅ 1. 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # 카테고리 테이블
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # 용어 테이블
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

    # 기본 카테고리
    categories = ['web', 'network', 'system', '기타']
    for cat in categories:
        c.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (cat,))
    
    conn.commit()
    conn.close()
    print("✅ 데이터베이스 초기화 완료")

# ✅ 2. 용어 추가
def add_term(title, content, category, author='unknown'):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('SELECT id FROM categories WHERE name = ?', (category,))
    row = c.fetchone()
    if not row:
        print(f"❌ '{category}' 카테고리가 없습니다.")
        conn.close()
        return False
    category_id = row[0]

    try:
        c.execute('''
            INSERT INTO terms (title, content, category_id, author, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, category_id, author, datetime.now()))
        conn.commit()
        print(f"✅ '{title}' 용어가 추가되었습니다.")
        return True
    except sqlite3.IntegrityError:
        print(f"❌ '{title}' 용어가 이미 존재합니다.")
        return False
    finally:
        conn.close()

# ✅ 3. 용어 수정
def edit_term(title, new_content, editor='unknown'):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('SELECT id FROM terms WHERE title = ?', (title,))
    if not c.fetchone():
        print(f"❌ '{title}' 용어가 없습니다.")
        conn.close()
        return False

    c.execute('''
        UPDATE terms
        SET content = ?, last_editor = ?, updated_at = ?
        WHERE title = ?
    ''', (new_content, editor, datetime.now(), title))
    conn.commit()
    conn.close()
    print(f"✅ '{title}' 용어가 수정되었습니다.")
    return True

# ✅ 4. 용어 삭제
def delete_term(title):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('DELETE FROM terms WHERE title = ?', (title,))
    conn.commit()
    deleted = c.rowcount
    conn.close()

    if deleted:
        print(f"✅ '{title}' 용어가 삭제되었습니다.")
        return True
    else:
        print(f"❌ '{title}' 용어를 찾을 수 없습니다.")
        return False

# ✅ 5. 용어 검색
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

    if results:
        for row in results:
            print(f"📚 제목: {row[0]}")
            print(f"🔖 카테고리: {row[2]} | 작성자: {row[3]} | 마지막 수정자: {row[4]}")
            print(f"📅 생성: {row[5]} | 수정: {row[6]}")
            print(f"내용 요약: {row[1][:60]}...")
            print("-" * 50)
    else:
        print("🔍 검색 결과가 없습니다.")

# ✅ 실행 테스트용
if __name__ == '__main__':
    init_db()

    # 테스트용 추가
    add_term("ZeroDay", "<h1>Zero-day</h1><p>패치 없는 취약점</p>", "기타", "admin")
    add_term("XSS", "<h1>XSS</h1><p>스크립트 삽입 공격</p>", "web", "admin")

    # 수정
    edit_term("XSS", "<h1>XSS</h1><p>웹 브라우저에서 실행되는 스크립트 공격입니다.</p>", "editor1")

    # 검색
    search_term("xss")

    # 삭제
    delete_term("ZeroDay")
