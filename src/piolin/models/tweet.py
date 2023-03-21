from piolin.db import db

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), db.ForeignKey('user.nickname'), nullable=False)
    text = db.Column(db.String(280), nullable=False)
    date = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Tweet {self.id}>'

