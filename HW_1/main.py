from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.get('/')
def first_page():
    return render_template('index.html')


@app.get('/clothes/')
def clothes():
    context = {'title':'Clothes',
               'content': 'Здесь когда-нибудь будет одежда'} 
    return render_template('page_1.html', **context)

@app.get('/shoes/')
def shoes():
    context = {'title':'Shoes',
               'content': 'А тут обувь'} 
    return render_template('page_2.html', **context)

@app.get('/jacket/')
def jacket():
    context = {'title':'Jacket',
               'content': 'Тут однажды увидим куртки'} 
    return render_template('page_3.html', **context)


if __name__ == '__main__':
    app.run()