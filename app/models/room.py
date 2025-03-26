from datetime import datetime
from app import db

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with reservations
    reservations = db.relationship('Reservation', backref='room', lazy=True)

    def __init__(self, name, capacity, location, description=None):
        self.name = name
        self.capacity = capacity
        self.location = location
        self.description = description

    def is_available(self, start_time, end_time, exclude_reservation_id=None):
        """Check if the room is available during the specified time period"""
        from app.models.reservation import Reservation

        # Base query for overlapping reservations
        query = Reservation.query.filter(
            Reservation.room_id == self.id,
            Reservation.status == 'approuvé',
            Reservation.end_time > start_time,
            Reservation.start_time < end_time
        )

        # Exclude a specific reservation if needed (for editing)
        if exclude_reservation_id:
            query = query.filter(Reservation.id != exclude_reservation_id)

        # Get all overlapping reservations
        overlapping_reservations = query.all()

        return len(overlapping_reservations) == 0

    def is_currently_available(self):
        """Check if the room is currently available"""
        now = datetime.utcnow()
        return self.is_available(now, now)

    def __repr__(self):
        return f"Room('{self.name}', Capacity: {self.capacity}, Location: '{self.location}')"
