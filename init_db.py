import sqlite3

def init_db():
    # 데이터베이스 파일 wiki.db 열기 (없으면 새로 생성)
    conn = sqlite3.connect('wiki.db')
    c = conn.cursor()

    # 카테고리 테이블 만들기
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # 용어 테이블 만들기
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

    # 기본 카테고리 데이터 넣기
    categories = ['web', 'network', 'system', '기타']
    for cat in categories:
        c.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (cat,))

    conn.commit()  # 변경사항 저장
    conn.close()   # DB 연결 닫기

    print("✅ 데이터베이스와 테이블 생성 완료!")

if __name__ == '__main__':
    init_db()
