from flask import Flask, url_for, render_template
from markupsafe import escape

# 实例化 Flask 类，创建一个 程序 对象 app
app = Flask(__name__)

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


# 视图函数(view function) -- 请求处理函数
@app.route('/')
def index():  # put application's code here
    # return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    return render_template('index.html', name=name, movies=movies)

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
