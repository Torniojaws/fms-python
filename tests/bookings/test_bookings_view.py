import json
import unittest

from app import app, db
from apps.bookings.models import Bookings
from apps.flights.models import Flights


class TestBookingsView(unittest.TestCase):
    def setUp(self):
        """Add some example entries to DB."""
        self.app = app.test_client()
        self.maxDiff = None

        # FIXME: These could also be mocked, but after doing some initial mocking, it turned out
        # quite complex to do for these cases. It was due to the way the queries interplay, so I
        # opted the more straightforward DB way for these simple tests. Normally these would of
        # course be mocked along with the DB responses. Those could have their own class method for
        # even better testability.

        # Create flights for bookings.
        # One way, no stopover
        flight1 = Flights(
            flight_number='AY1234',
            departure='HEL',
            arrival='ARN',
            departure_date='2016-02-04 06:08:00',
            arrival_date='2016-02-04 07:08:00',
        )
        # Return trip, no stopover
        flight2 = Flights(
            flight_number='AY5432',
            departure='HEL',
            arrival='AMS',
            departure_date='2017-08-05 10:05:00',
            arrival_date='2017-08-05 11:35:00',
        )
        flight3 = Flights(
            flight_number='AY98',
            departure='AMS',
            arrival='HEL',
            departure_date='2017-08-09 13:00:00',
            arrival_date='2017-08-09 15:05:00',
        )
        # Return trip with stopovers
        flight4 = Flights(
            flight_number='AY5432',
            departure='HEL',
            arrival='AMS',
            departure_date='2018-08-05 10:05:00',
            arrival_date='2018-08-05 11:35:00',
        )
        flight5 = Flights(
            flight_number='AY98',
            departure='AMS',
            arrival='HKG',
            departure_date='2018-08-05 13:00:00',
            arrival_date='2018-08-06 07:05:00',
        )
        flight6 = Flights(
            flight_number='AY99',
            departure='HKG',
            arrival='AMS',
            departure_date='2018-09-05 10:05:00',
            arrival_date='2018-09-05 19:35:00',
        )
        flight7 = Flights(
            flight_number='AY5431',
            departure='AMS',
            arrival='HEL',
            departure_date='2018-09-05 23:00:00',
            arrival_date='2018-09-06 01:05:00',
        )
        db.session.add(flight1)
        db.session.add(flight2)
        db.session.add(flight3)
        db.session.add(flight4)
        db.session.add(flight5)
        db.session.add(flight6)
        db.session.add(flight7)
        db.session.commit()

        # Add 3 bookings for passenger_id 4321
        # The first booking has no stopover and no return flight
        booking1 = Bookings(
            booking_id='ABCDEF',
            flight_number='AY1234',
            passenger_id=4321,
            first_name='Testi',
            last_name='Testinen',
            email='test@example.com'
        )
        # The second booking has no stopover and has a return flight
        booking2 = Bookings(
            booking_id='XYZUVW',
            flight_number='AY5432',
            passenger_id=4321,
            first_name='Testi',
            last_name='Testinen',
            email='test@example.com'
        )
        booking3 = Bookings(
            booking_id='XYZUVW',
            flight_number='AY98',
            passenger_id=4321,
            first_name='Testi',
            last_name='Testinen',
            email='test@example.com'
        )
        # The third booking has one stopover and a return flight
        booking4 = Bookings(
            booking_id='FOOBAR',
            flight_number='AY5432',
            passenger_id=4321,
            first_name='Testi',
            last_name='Testinen',
            email='test@example.com'
        )
        booking5 = Bookings(
            booking_id='FOOBAR',
            flight_number='AY98',
            passenger_id=4321,
            first_name='Testi',
            last_name='Testinen',
            email='test@example.com'
        )
        booking6 = Bookings(
            booking_id='FOOBAR',
            flight_number='AY99',
            passenger_id=4321,
            first_name='Testi',
            last_name='Testinen',
            email='test@example.com'
        )
        booking7 = Bookings(
            booking_id='FOOBAR',
            flight_number='AY5431',
            passenger_id=4321,
            first_name='Testi',
            last_name='Testinen',
            email='test@example.com'
        )
        db.session.add(booking1)
        db.session.add(booking2)
        db.session.add(booking3)
        db.session.add(booking4)
        db.session.add(booking5)
        db.session.add(booking6)
        db.session.add(booking7)
        db.session.commit()

    def tearDown(self):
        """Cleanup"""
        for flight in Flights.query.all():
            db.session.delete(flight)
        for booking in Bookings.query.all():
            db.session.delete(booking)
        db.session.commit()

    def test_getting_bookings_by_uid(self):
        """Eg. GET /bookings?uid=4321
        Gets all bookings the UID has and lists them in ascending order.
        NB: this endpoint checks for bookings.passenger_id, not bookings.id
        """
        response = self.app.get('/bookings?uid=4321')
        bookings = json.loads(response.get_data().decode())

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(bookings), 7)
        self.assertEquals(bookings, [{
            'bookingId': 'ABCDEF',
            'lastName': 'Testinen',
            'departure': 'HEL',
        }, {
            'bookingId': 'XYZUVW',
            'lastName': 'Testinen',
            'departure': 'HEL',
        }, {
            'bookingId': 'XYZUVW',
            'lastName': 'Testinen',
            'departure': 'AMS',
        }, {
            'bookingId': 'FOOBAR',
            'lastName': 'Testinen',
            'departure': 'HEL',
        }, {
            'bookingId': 'FOOBAR',
            'lastName': 'Testinen',
            'departure': 'AMS',
        }, {
            'bookingId': 'FOOBAR',
            'lastName': 'Testinen',
            'departure': 'HKG',
        }, {
            'bookingId': 'FOOBAR',
            'lastName': 'Testinen',
            'departure': 'AMS',
        }])

    def test_getting_passenger_bookings_with_return_flights_by_uid(self):
        """Eg. GET /bookings?uid=4321&withReturnFlights=true
        Gets all bookings the passenger has that also have return flights, in ascending order."""
        # NB: this endpoint checks for bookings.passenger_id, not bookings.id
        response = self.app.get('/bookings?uid=4321&withReturnFlights=true')
        bookings = json.loads(response.get_data().decode())

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(bookings), 6)
        self.assertEquals(bookings, [{
            'bookingId': 'XYZUVW',
            'lastName': 'Testinen',
            'departure': 'HEL',
        }, {
            'bookingId': 'XYZUVW',
            'lastName': 'Testinen',
            'departure': 'AMS',
        }, {
            'bookingId': 'FOOBAR',
            'lastName': 'Testinen',
            'departure': 'HEL',
        }, {
            'bookingId': 'FOOBAR',
            'lastName': 'Testinen',
            'departure': 'AMS',
        }, {
            'bookingId': 'FOOBAR',
            'lastName': 'Testinen',
            'departure': 'HKG',
        }, {
            'bookingId': 'FOOBAR',
            'lastName': 'Testinen',
            'departure': 'AMS',
        }])

    def test_getting_a_booking_by_nonexisting_uid(self):
        """Eg. GET /bookings?uid=1111"""
        # NB: this endpoint checks for bookings.passenger_id, not bookings.id
        response = self.app.get('/bookings?uid=1111')
        booking = json.loads(response.get_data().decode())
        self.assertEquals(404, response.status_code)
        self.assertEquals(booking, {
            'success': False,
            'message': 'No bookings were found for passenger ID 1111',
        })

    def test_getting_a_booking_by_booking_id(self):
        """Eg. GET /bookings/XYZUVW"""
        response = self.app.get('/bookings/XYZUVW')
        booking = json.loads(response.get_data().decode())
        self.assertEquals(200, response.status_code)
        self.assertEquals(booking, {
            'id': 'XYZUVW',
            'passenger': {
                'firstName': 'Testi',
                'lastName': 'Testinen',
                'email': 'test@example.com',
            },
            'flights': [{
                'departure': 'HEL',
                'arrival': 'AMS',
                'departureDate': '2017-08-05 10:05:00',
                'arrivalDate': '2017-08-05 11:35:00',
            }, {
                'departure': 'AMS',
                'arrival': 'HEL',
                'departureDate': '2017-08-09 13:00:00',
                'arrivalDate': '2017-08-09 15:05:00',
            }]
        })
