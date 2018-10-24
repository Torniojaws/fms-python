from flask import jsonify, make_response, request
from flask_classful import FlaskView
from sqlalchemy import asc, desc

from apps.bookings.models import Bookings
from apps.flights.models import Flights
from apps.utils.time import get_iso_format


class BookingsView(FlaskView):
    # GET /bookings?uid=4321&withReturnFlights=true
    def index(self):
        uid = request.args.get('uid', '')
        with_return_flight = request.args.get('withReturnFlights', 'false')

        check_flight = False
        if with_return_flight == 'true':
            # Return only bookings that have a return flight
            check_flight = True

        # All bookings the passenger has ever done
        bookings = Bookings.query.filter_by(passenger_id=uid).all()
        print(bookings)
        if not bookings:
            return make_response(jsonify({
                'success': False,
                'message': 'No bookings were found for passenger ID {}'.format(uid)
            }), 404)

        flights = []
        for booking in bookings:
            print('It returns {}'.format(Flights.query.filter_by()))
            booking_flight_number = booking.get('flight_number', '')
            first_flight = Flights.query.filter_by(flight_number=booking_flight_number).order_by(
                asc(Flights.departure_date)).first()
            flight = {
                'bookingId': booking.booking_id,
                'lastName': booking.last_name,
                'departure': first_flight.departure,
            }
            if check_flight:
                last_flight = Flights.query.filter_by(flight_number=booking.flight_number).order_by(
                    desc(Flights.departure_date)).first()
                if first_flight.departure == last_flight.arrival:
                    flights.append(flight)
                continue
            else:
                flights.append(flight)

        if not first_flight:
            return make_response(jsonify({
                'success': True,
                'message': 'No flight was found for passenger ID {}'.format(uid)
            }), 200)

        return make_response(jsonify(flights), 200)

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
