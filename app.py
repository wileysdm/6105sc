from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)  # 允许跨域请求

# 数据库路径
DATABASE = 'database.db'

def query_database(query, args=(), one=False):
    """执行 SQLite 查询"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_papers():
    """根据关键字搜索论文"""
    keyword = request.args.get('query', '').strip()  # 去掉多余空格
    if not keyword:
        return jsonify({'results': []})

    try:
        # 查询论文基本信息及关联作者
        query = """
            SELECT 
                p.title, 
                p.abstract, 
                p.DID, 
                p.timestamp, 
                p.keywords,
                GROUP_CONCAT(a.nickname, ', ') AS authors  -- 聚合作者名称
            FROM paper p
            LEFT JOIN paper_authors pa ON p.DID = pa.DID
            LEFT JOIN account a ON pa.author_id = a.account_id
            WHERE LOWER(p.title) LIKE LOWER(?) 
               OR LOWER(p.abstract) LIKE LOWER(?) 
               OR LOWER(p.keywords) LIKE LOWER(?)
            GROUP BY p.DID;
        """
        args = [f'%{keyword}%'] * 3  # 只匹配论文的关键词、标题、摘要
        results = query_database(query, args)

        # 转换结果为 JSON 格式
        data = [
            {
                'title': row['title'],
                'abstract': row['abstract'],
                'DID': row['DID'],
                'timestamp': row['timestamp'],
                'keywords': row['keywords'],
                'authors': row['authors']  # 作者列表（以逗号分隔）
            }
            for row in results
        ]
        return jsonify({'results': data})

    except Exception as e:
        # 打印错误日志
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
