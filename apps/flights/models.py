from app import db


class Flights(db.Model):
    """The model for flights."""
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(6), nullable=False)
    departure = db.Column(db.String(3))
    arrival = db.Column(db.String(3))
    departure_date = db.Column(db.DateTime)
    arrival_date = db.Column(db.DateTime)
