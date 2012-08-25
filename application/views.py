from application import app
from flask import render_template, redirect, request, session, url_for, abort, flash
from flaskext.markdown import Markdown
from flask import g

from models import Comment
from forms import CommentForm
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
    Along with the comments.
    """
    # get current comment errors in g.error_form
    if hasattr(g, 'error_form'):
        form = g.error_form
        del g.error_form
    else:
        form = CommentForm(request.form)
    # We don't need no g
    for article in ARTICLES:
        if article["slug"] == slug:
            # The article has been found.
            q = Comment.all()
            # filter the comments connected to the slug
            q.filter("slug =", slug)
            # order the comments by date
            q.order('when')
            # fetch the first 50 comments
            comments = q.fetch(50)
            return render_template("post.html", post = article, form = form,
                                   comments = comments)
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
    archive = [(a['title'], a['slug'], a['date']) for a in ARTICLES]
    return render_template("archive.html", archive = archive)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404      


@app.route('/post-comment', methods = ['GET', 'POST'])
def post_comment():
    """
    Handles request to post a comment.
    """
    form = CommentForm(request.form)
    if request.method == 'POST':
        if form.validate():
            comment = Comment(slug = form.slug.data,
                              body = form.comment.data,
                              author = form.name.data,
                              email = form.email.data)
            comment.put()
            flash("Some comment data posted and saved")
            # TODO: change to the slug url once slug is obtained
            return redirect(url_for('show_post', slug=form.slug.data))
        else:
            flash("There was an error with the form")
            # I am storing the error form in the global object
            # will decide on a better way later
            g.error_form = form 
            return redirect(url_for('show_post', slug=form.slug.data))

    flash('DID NOT WORK')
    return redirect(url_for('show_index'))
    


    
