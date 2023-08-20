from flask import render_template, Flask, jsonify, request
from application import app
from main import fetch_books, format_and_print_books
from input import format_category_for_search

@app.route('/')
@app.route('/index')
@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html', title='Chapter One')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/FAQ')
def FAQ():
    return render_template('faq.html', title='FAQ')


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
