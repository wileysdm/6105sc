from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库路径
DATABASE = 'your-database-name.db'

def query_database(query, args=(), one=False):
    """执行 SQLite 查询"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/search', methods=['GET'])
def search_papers():
    """根据关键字搜索论文"""
    keyword = request.args.get('query', '')
    if not keyword:
        return jsonify({'results': []})

    query = """
        SELECT p.title, p.abstract, p.DID, p.timestamp, p.keywords, a.nickname AS author_name
        FROM paper p
        INNER JOIN author au ON p.DID = au.DID
        INNER JOIN account a ON au.author_id = a.account_id
        WHERE p.title LIKE ? OR p.abstract LIKE ? OR p.keywords LIKE ? OR a.nickname LIKE ?;
    """
    args = [f'%{keyword}%'] * 4
    results = query_database(query, args)
    
    # 转换结果为 JSON 格式
    data = [
        {
            'title': row['title'],
            'abstract': row['abstract'],
            'DID': row['DID'],
            'timestamp': row['timestamp'],
            'keywords': row['keywords'],
            'author_name': row['author_name']
        }
        for row in results
    ]
    return jsonify({'results': data})

if __name__ == '__main__':
    app.run(debug=True)
