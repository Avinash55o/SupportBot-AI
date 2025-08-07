from . import db
import uuid
from datetime import datetime

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(15), unique=True, nullable=False, default=lambda: f"TKT-{datetime.now().strftime('%y%m%d')}-{str(uuid.uuid4())[:4].upper()}")
    issue_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='open')
    priority = db.Column(db.String(50), default='normal')
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned_admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __init__(self, **kwargs):
        super(Ticket, self).__init__(**kwargs)
        if not self.token:
            # Generate a more compact token format: TKT-YYMMDD-XXXX
            # This gives us exactly 15 characters: TKT-YYMMDD-XXXX
            self.token = f"TKT-{datetime.now().strftime('%y%m%d')}-{str(uuid.uuid4())[:4].upper()}"

    def to_dict(self):
        return {
            "id": self.id,
            "token": self.token,
            "issue_type": self.issue_type,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
            "assigned_admin_id": self.assigned_admin_id
        }