import sqlite3
from contextlib import contextmanager

# 假設執行目錄在專案根目錄
DATABASE = 'instance/database.db'

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    # 讓查詢結果能透過欄位名稱存取（類似字典）
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

class Spot:
    @staticmethod
    def create(name, location='', notes='', category='', tags=''):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO spots (name, location, notes, category, tags)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (name, location, notes, category, tags)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all(keyword=None):
        with get_db() as conn:
            if keyword:
                search = f"%{keyword}%"
                cursor = conn.execute(
                    '''
                    SELECT * FROM spots 
                    WHERE name LIKE ? OR location LIKE ? OR category LIKE ? OR tags LIKE ?
                    ORDER BY created_at DESC
                    ''', 
                    (search, search, search, search)
                )
            else:
                cursor = conn.execute('SELECT * FROM spots ORDER BY created_at DESC')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(spot_id):
        with get_db() as conn:
            cursor = conn.execute('SELECT * FROM spots WHERE id = ?', (spot_id,))
            return cursor.fetchone()

    @staticmethod
    def update(spot_id, name, location='', notes='', category='', tags=''):
        with get_db() as conn:
            conn.execute(
                '''
                UPDATE spots 
                SET name = ?, location = ?, notes = ?, category = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                ''',
                (name, location, notes, category, tags, spot_id)
            )
            conn.commit()

    @staticmethod
    def delete(spot_id):
        with get_db() as conn:
            conn.execute('DELETE FROM spots WHERE id = ?', (spot_id,))
            conn.commit()
