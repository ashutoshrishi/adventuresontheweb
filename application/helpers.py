from application import app

import re
import os
import yaml
import glob
import datetime

#ARTICLES_DIR = app.config['ARTICLES_DIR']
ARTICLES_DIR = 'application/articles/'

def get_date(title):
    """Generates a datetime object from the post title.
    
    The post title is in the form YYYY-MM-DD-post-title.
    """
    title = os.path.split(title)[1]
    year = int(title[:4])
    month = int(title[5:7])
    day = int(title[8:10])
    d = datetime.datetime(year, month, day)
    return d    


def sorted_listing(path):
    """Returns a list of yaml files sorted by time. """
    date = lambda f: get_date(f)
    return list(sorted(glob.glob(os.path.join(path, '*.yaml')), key = date))


def get_articles():
    """
    Make a list of Articles
    """
    articles = []
    for file in sorted_listing('application/articles/'):
            with open(file, 'r') as f:
                article = yaml.load(f.read())

                # posts can provide a slug of their own
                if not hasattr(article, 'slug'):
                    article['slug'] = slugify(article["title"])
                
                # Make a summary is the article is too long
                if len(article['body']) > 4000:
                    article['summary'] = shorten(article['body'])
                    
                articles.append(article)
    
    articles.reverse()
    return articles
    
def shorten(body):
    """
    Creates a summary of a long post.
    """
    next_line = body[4000:].index('\n') + 4000
    return body[:(next_line-1)] + " . . ."
    
    
def slugify(url):
    """
    Generates slugs for posts 
    """
    return re.sub(r'-$', '', re.sub(r'[^A-Za-z0-9\-]+', '-', url.lower()))
                
    
