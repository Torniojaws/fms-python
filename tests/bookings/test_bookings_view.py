import json
import unittest

from app import app, db
from apps.bookings.models import Bookings
from apps.flights.models import Flights


class TestBookingsView(unittest.TestCase):
    def setUp(self):
        """Add some example entries to DB."""
        self.app = app.test_client()

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
            id='123',
            flight_number='AY131',
            passenger_id='4321',
            first_name='Test1',
            last_name='Test1nen',
            email='test1@example.com',
        )
        booking2 = Bookings(
            id='124',
            flight_number='AY5003',
            passenger_id='4321',
            first_name='Test1',
            last_name='Test1nen',
            email='test1@example.com',
        )
        booking3 = Bookings(
            id='444',
            flight_number='AY5003',
            passenger_id='2323',
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
        """Eg. GET /bookings?uid=123"""
        response = self.app.get('/bookings?uid=123')
        booking = json.loads(response.get_data().decode())
        self.assertEquals(200, response.status_code)
        self.assertEquals(booking, {
            'bookingId': 123,
            'lastName': 'Test1nen',
            'departure': 'HEL',
        })
