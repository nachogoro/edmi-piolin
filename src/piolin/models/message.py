from piolin.db import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), db.ForeignKey('user.nickname'), nullable=False)
    receiver = db.Column(db.String(80), db.ForeignKey('user.nickname'), nullable=False)
    body = db.Column(db.String(280), nullable=False)
    date = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Message {self.id}>'

