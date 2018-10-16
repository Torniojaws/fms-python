

from flask import jsonify, make_response, request
from flask_classful import FlaskView
from sqlalchemy import asc

from apps.bookings.models import Bookings
from apps.flights.models import Flights


class BookingsView(FlaskView):
    # GET /bookings?uid=123
    def index(self):
        uid = request.args.get('uid', '')
        booking = Bookings.query.filter_by(passenger_id=uid).first_or_404()
        first_flight = Flights.query.filter_by(booking.flight_number).order_by(
            asc(Flights.departure_date)).first_or_404()

        contents = jsonify({
            'bookingId': booking.id,
            'lastName': booking.last_name,
            'departure': first_flight.departure,
        })

        return make_response(contents, 200)

    # GET /bookings/:id/
    def get(self, booking_id):
        # Assumes that each flight has its own booking for the passenger
        bookings = Bookings.query.filter_by(id=booking_id).all()
        flights = []
        for booking in bookings:
            flight = Flights.query.filter_by(flight_number=booking.flight_number).first()
            if flight:
                flights.add(flight)
            else:
                print('No such flight found')

        contents = jsonify({
            'id': booking_id,
            'passenger': {
                'firstName': booking.first_name,
                'lastName': booking.last_name,
                'email': booking.email,
            },
            'flights': flights,
        })

        return make_response(contents, 200)
