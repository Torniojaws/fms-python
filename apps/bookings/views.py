from flask import jsonify, make_response, request
from flask_classful import FlaskView
from sqlalchemy import asc

from apps.bookings.models import Bookings
from apps.flights.models import Flights
from apps.utils.time import get_iso_format


class BookingsView(FlaskView):
    # GET /bookings?uid=4321
    def index(self):
        uid = request.args.get('uid', '')
        booking = Bookings.query.filter_by(passenger_id=uid).first()
        if not booking:
            return make_response(jsonify({
                'success': True,
                'message': 'No booking was found for passenger ID {}'.format(uid)
            }), 200)

        first_flight = Flights.query.filter_by(flight_number=booking.flight_number).order_by(
            asc(Flights.departure_date)).first()
        if not first_flight:
            return make_response(jsonify({
                'success': True,
                'message': 'No flight was found for passenger ID {}'.format(uid)
            }), 200)

        contents = jsonify({
            'bookingId': booking.booking_id,
            'lastName': booking.last_name,
            'departure': first_flight.departure,
        })

        return make_response(contents, 200)

    # GET /bookings/:id/
    def get(self, booking_id):
        # Assumes that each flight has its own booking for the passenger
        bookings = Bookings.query.filter_by(booking_id=booking_id).all()
        if not bookings:
            return make_response(
                jsonify({'success': True, 'message': 'No booking by ID {} was found'.format(
                    booking_id)}),
                200
            )
        flights = []
        for booking in bookings:
            flight = Flights.query.filter_by(flight_number=booking.flight_number).first()
            if flight:
                flights.append({
                    'departure': flight.departure,
                    'arrival': flight.arrival,
                    'departureDate': get_iso_format(flight.departure_date),
                    'arrivalDate': get_iso_format(flight.arrival_date),
                })
            else:
                print('No such flight found')

        contents = jsonify({
            'id': booking_id,
            'passenger': {
                'firstName': bookings[0].first_name,
                'lastName': bookings[0].last_name,
                'email': bookings[0].email,
            },
            'flights': flights,
        })

        return make_response(contents, 200)
