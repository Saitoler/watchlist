from flask import Flask, url_for, render_template
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import click

# 实例化 Flask 类，创建一个 程序 对象 app
app = Flask(__name__)

# 设置数据库连接地址
mysql_url = "mysql+pymysql://root:wxc.469713@127.0.0.1:3306/watchlist"
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 是否追踪数据库修改, 一般不开启，会影响性能

# 初始化 db, 关联 flask 项目
db = SQLAlchemy(app)

name = "Saitoler"
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


# 创建数据库模型
class User(db.Model):  # 表名将会是 user (自动生成，小写处理)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# 自定义命令 initdb 用于初始化 db
@app.cli.command()  # 注册为命令 可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置命令行选项
def initdb(drop):
    if drop:
        db.drop_all()

    db.create_all()
    click.echo("已初始化数据库")


# 自定义命令用于将虚拟数据添加到数据库里
@app.cli.command()
def forge():
    db.create_all()

    # 将 User 写入 db
    user = User(name=name)
    db.session.add(user)

    # 将 movie 写入 db
    for movie in movies:
        movie = Movie(title=movie['title'], year=movie['year'])
        db.session.add(movie)

    # 提交数据
    db.session.commit()
    click.echo("虚拟数据已写入数据库中.")


# 视图函数(view function) -- 请求处理函数
@app.route('/')
def index():  # put application's code here
    # return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    return render_template('index.html', name=name, movies=movies)


# 404处理函数， 作为统一的 404 错误页面进行返回
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 这个装饰器可以注册一个模板上下文处理函数， 对于多个模板内都需要使用的变量就不需要在每个模板里重复去查询了
@app.context_processor
def get_user_info():
    user = User.query.first()
    return dict(user=user)  # 这里需要返回一个字典类型，相当于 return {"user": user}


@app.route('/home')
def home():  # put application's code here
    return '这是 watchlist 的 home 页面！'


@app.route('/user/<name>')
def user_page(name):
    # escape 用于对用户输入进行转义处理，避免用户输入包含恶意代码时，浏览器将用户输入当做代码执行
    return f'User:{escape(name)}'


@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='saitoler'))
    print(url_for('user_page', name='Jenny'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))

    return "Test Page"


if __name__ == '__main__':
    app.run()
