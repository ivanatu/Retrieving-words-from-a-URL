from app import db, url_app
from werkzeug.security import generate_password_hash
# from sqlalchemy.dialects.postgresql import JSON
# import psycopg2

class Url(db.Model):
    __tablename__ = "url"
    id = db.Column(db.String(128), primary_key=True)
    # id_salted = db.Column(db.String(64), index=True, unique=True)
    # username = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(1200))
    word_count = db.Column(db.Integer)

    def __init__(self, id, username, word_count):
        self.username = username
        self.word_count = word_count

    def set_word(self, username):
        self.word_hash = generate_password_hash(username)

    def __repr__(self):
        return '<id %r>' % self.username    