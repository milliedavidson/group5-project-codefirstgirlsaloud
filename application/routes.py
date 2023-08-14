from flask import render_template
from application import app


@app.route('/')
@app.route('/index')
@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/FAQ')
def FAQ():
    return render_template('faq.html', title='FAQ')


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
