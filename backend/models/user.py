from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # User's own tickets (created by them)
    tickets = db.relationship('Ticket', 
                             foreign_keys='Ticket.user_id',
                             backref='user', 
                             lazy=True)
    
    # Tickets assigned to this admin
    assigned_tickets = db.relationship('Ticket', 
                                      foreign_keys='Ticket.assigned_admin_id',
                                      backref='assigned_admin', 
                                      lazy=True)