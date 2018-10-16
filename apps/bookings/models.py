from app import db


class Bookings(db.Model):
    """The model for bookings."""
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(6))
    flight_number = db.Column(db.String(6))
    passenger_id = db.Column(db.Integer)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
