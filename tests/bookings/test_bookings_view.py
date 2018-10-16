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

        flight1 = Flights(
            flight_number='AY131',
            departure='HEL',
            arrival='SIN',
            departure_date='2018-10-16 23:55:00',
            arrival_date='2018-10-17 17:15:00',
        )
        flight2 = Flights(
            flight_number='AY5003',
            departure='SIN',
            arrival='SYD',
            departure_date='2018-10-17 19:15:00',
            arrival_date='2018-10-18 06:15:00',
        )
        db.session.add(flight1)
        db.session.add(flight2)
        db.session.commit()

        booking1 = Bookings(
            booking_id='ABCXYZ',
            flight_number='AY131',
            passenger_id=4321,
            first_name='Test1',
            last_name='Test1nen',
            email='test1@example.com',
        )
        booking2 = Bookings(
            booking_id='ABCXYZ',
            flight_number='AY5003',
            passenger_id=4321,
            first_name='Test1',
            last_name='Test1nen',
            email='test1@example.com',
        )
        booking3 = Bookings(
            booking_id='YYYZZZ',
            flight_number='AY5003',
            passenger_id=2323,
            first_name='Test2',
            last_name='Test2nen',
            email='test2@example.com',
        )
        db.session.add(booking1)
        db.session.add(booking2)
        db.session.add(booking3)
        db.session.commit()

    def tearDown(self):
        """Clean up."""
        for flight in Flights.query.all():
            db.session.delete(flight)
        for booking in Bookings.query.all():
            db.session.delete(booking)
        db.session.commit()

    def test_getting_a_booking_by_uid(self):
        """Eg. GET /bookings?uid=4321"""
        # NB: this endpoint checks for bookings.passenger_id, not bookings.id
        response = self.app.get('/bookings?uid=4321')
        booking = json.loads(response.get_data().decode())
        expected_booking_id = Bookings.query.filter_by(passenger_id=4321).first().booking_id
        self.assertEquals(200, response.status_code)
        self.assertEquals(booking, {
            'bookingId': expected_booking_id,
            'lastName': 'Test1nen',
            'departure': 'HEL',
        })

    def test_getting_a_booking_by_nonexisting_uid(self):
        """Eg. GET /bookings?uid=1111"""
        # NB: this endpoint checks for bookings.passenger_id, not bookings.id
        response = self.app.get('/bookings?uid=1111')
        booking = json.loads(response.get_data().decode())
        self.assertEquals(200, response.status_code)
        self.assertEquals(booking, {
            'success': True,
            'message': 'No booking was found for passenger ID 1111',
        })

    def test_getting_a_booking_by_booking_id(self):
        """Eg. GET /bookings/ABCXYZ"""
        response = self.app.get('/bookings/ABCXYZ')
        booking = json.loads(response.get_data().decode())
        self.assertEquals(200, response.status_code)
        self.assertEquals(booking, {
            'id': 'ABCXYZ',
            'passenger': {
                'firstName': 'Test1',
                'lastName': 'Test1nen',
                'email': 'test1@example.com',
            },
            'flights': [{
                'departure': 'HEL',
                'arrival': 'SIN',
                'departureDate': '2018-10-16 23:55:00',
                'arrivalDate': '2018-10-17 17:15:00',
            }, {
                'departure': 'SIN',
                'arrival': 'SYD',
                'departureDate': '2018-10-17 19:15:00',
                'arrivalDate': '2018-10-18 06:15:00',
            }]
        })
