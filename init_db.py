# init_db.py
import sqlite3

# wiki.db라는 파일로 데이터베이스를 만든다 (없으면 새로 생성됨)
conn = sqlite3.connect('wiki.db')
c = conn.cursor()

# terms라는 이름의 테이블을 만든다 (보안 용어 저장용)
c.execute('''
    CREATE TABLE IF NOT EXISTS terms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        content TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT
    )
''')

# 변경사항 저장 후 DB 연결 종료
conn.commit()
conn.close()

print("✅ 데이터베이스 초기화 완료!")
