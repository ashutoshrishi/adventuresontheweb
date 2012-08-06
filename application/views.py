from application import app
from flask import render_template, redirect, request, session, url_for, abort, flash
from flaskext.markdown import Markdown

from helpers import get_articles

app.config['ARTICLES'] = get_articles()


ARTICLES = app.config['ARTICLES']
ARTICLES_DIR = app.config['ARTICLES_DIR']

md = Markdown(app, extensions = ['codehilite'])

@app.route('/')
def show_index():
    """
    Rendering the front page, show all posts from articles dir.
    """
    flash("Welcome!")
    return render_template("content.html", posts = ARTICLES)


@app.route('/posts/<slug>', methods=['GET'])
def show_post(slug):
    """
    Find the currect article by slug and display it.
    """
    for article in ARTICLES:
        if article["slug"] == slug:
            return render_template("post.html", post = article)
    return abort(404)

@app.route('/posts/', methods=['GET'])
def show_archive():
    return render_template("archive_posts.html")

@app.route('/posts/<int:year>/', methods=['GET'])
def show_post_year(year):
    """
    Return lists of post of that year.
    """
    matched = []
    for article in ARTICLES:
        if article['date'].year == year:
            matched.append(article)
    return render_template("archive_posts_year.html", matched = matched)

@app.route('/posts/<int:year>/<int:month>/', methods=['GET'])
def show_post_year_month(year, month):
    """
    Return list of post by year and month
    """
    matched = []
    for article in ARTICLES:
        if article['date'].year == year:
            if article['date'].month == month:
                matched.append(article)    
    return render_template("archive_posts.html", matched = matched)

@app.route('/archive/', methods=['GET'])
def show_archive():
    return render_template("archive.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404      

