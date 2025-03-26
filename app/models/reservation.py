from datetime import datetime
from app import db

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='en attente')  # pending, approved, rejected

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    # Optional: admin who approved/rejected the reservation
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    admin = db.relationship('User',
                           foreign_keys=[admin_id],
                           backref=db.backref('handled_reservations', lazy=True))

    def __init__(self, title, description, start_time, end_time, user_id, room_id):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.user_id = user_id
        self.room_id = room_id

    def approve(self, admin_id):
        self.status = 'approuvé'
        self.admin_id = admin_id

    def reject(self, admin_id):
        self.status = 'rejeté'
        self.admin_id = admin_id

    def is_active(self):
        now = datetime.utcnow()
        return self.status == 'approuvé' and self.start_time <= now <= self.end_time

    def __repr__(self):
        return f"Reservation('{self.title}', Status: {self.status}, Room: {self.room_id}, User: {self.user_id})"
