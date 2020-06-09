# 导入所需模块和方法
import sqlite3
from flask import (Flask, render_template, g, flash, request, session, abort,
        redirect, url_for)

# 配置项
DATABASE = '/tmp/flaskr.db'
ENV = 'development'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# 创建应用
app = Flask(__name__)
# app.config 的 from_object 方法通常用于获取对象的属性以增加配置项
# 此处使用的参数为 __name__ ，也就是当前所在文件
# 结果就是读取当前所在文件中的所有变量，选择其中全大写的变量作为配置项
app.config.from_object(__name__)

# 此函数的返回值是 sqlite3.connect 方法的调用，也就是连接对象
# 这里之所以写一个函数，是因为后面的代码会多次用到连接对象
def db_conn():
    '''创建与数据库连接的对象
    '''

    return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
    app.run()

def init_db():
    '''此函数用于创建数据表，需要在 flask shell 里引入执行
    '''

    with db_conn() as conn:
        with app.open_resource('schema.sql') as f:
            conn.cursor().executescript(f.read().decode())
        conn.commit()

# 这个装饰器的功能是，当任意视图函数执行时，预先执行这个装饰器下的所有函数
@app.before_request
def before():
    '''创建数据库的连接对象，并将其赋值给 g 的 conn 属性
    '''

    g.conn = db_conn()

@app.teardown_request
def teardown(exception):
    '''关闭与数据库的连接
    '''

    g.conn.close()

@app.route('/')
def show_entries():
    '''显示所有存储在数据表中的条目
    '''

    # 获取连接对象执行查询操作之后的光标对象，该对象的 fetchall 方法中存储了查询结果
    cursor = g.conn.execute('SELECT title, text FROM entries ORDER BY id DESC')
    # 查询结果是一个列表，列表里是元组，将元组转换成字典
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    '''添加一条博客
    '''

    if not session.get('login'):
        abort(401)
    g.conn.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
            [request.form.get('title'), request.form.get('text')])
    g.conn.commit()
    flash('New entry has beensuccessfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''用户登录
    '''

    error = None
    if request.method == 'POST':
        # 如果用户名与配置项不符
        if request.form.get('username') != app.config.get('USERNAME'):
            error = 'Invalid username'
        # 如果密码与配置项不符
        elif request.form.get('password') != app.config.get('PASSWORD'):
            error = 'Invalid password'
        else:
            session['login'] = True
            flash('You\'re loginned successfully!')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    '''用户登出
    '''

    session.pop('login', None)
    flash('You have logouted successfully')
    return redirect(url_for('show_entries'))

