from google.appengine.ext import db

class Comment(db.Model):
    slug = db.StringProperty(required=True)
    body = db.TextProperty()
    when = db.DateTimeProperty(auto_now_add = True)
    author = db.StringProperty(required=True)
    email = db.StringProperty()
    
