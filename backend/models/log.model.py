from . import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=True)