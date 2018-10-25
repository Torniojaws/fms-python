from flask import jsonify, make_response, request
from flask_classful import FlaskView
from sqlalchemy import asc  # , desc

from apps.bookings.models import Bookings
from apps.flights.models import Flights
from apps.utils.time import get_iso_format


class BookingsView(FlaskView):
    # GET /bookings?uid=4321&withReturnFlights=true
    def index(self):
        uid = request.args.get('uid', '')
        with_return_flight = request.args.get('withReturnFlights', 'false')
        check_flight = with_return_flight == 'true'  # Converts param to matching boolean

        # All bookings the passenger has ever done
        bookings = Bookings.query.filter_by(passenger_id=uid).all()
        if not bookings:
            return make_response(jsonify({
                'success': False,
                'message': 'No bookings were found for passenger ID {}'.format(uid)
            }), 404)

        # All flights for the current passenger, oldest first
        passenger_flight_numbers = [b.flight_number for b in bookings]
        all_flights = Flights.query.filter(
            Flights.flight_number.in_(passenger_flight_numbers)
        ).order_by(
            asc(Flights.departure_date)
        ).all()

        result = []
        for booking in bookings:
            # Here we rely on the order of flights being in ascending order, so we don't mix up
            # two different flights with the same number but different departure dates, although
            # in this case it wouldn't matter as the departure airport is the same anyway.
            current_flight = [f for f in all_flights if f.flight_number == booking.flight_number]
            flight = {
                'bookingId': booking.booking_id,
                'lastName': booking.last_name,
                'departure': current_flight[0].departure,
            }
            if check_flight:
                # withReturnFlights=true, ie. checking only for bookings with return flights
                # Defined as a booking whose first flight departs from the same airport as where
                # the last flight arrives to.
                current_bookings = [b for b in bookings if b.booking_id == booking.booking_id]

                first_flight_number = current_bookings[0].flight_number
                first_flight = [f for f in all_flights if f.flight_number == first_flight_number]

                last_flight_number = current_bookings[-1].flight_number
                last_flight = [f for f in all_flights if f.flight_number == last_flight_number]

                if first_flight[0].departure == last_flight[0].arrival:
                    result.append(flight)

            else:
                result.append(flight)

        return make_response(jsonify(result), 200)

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
