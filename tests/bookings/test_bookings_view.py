import json
import unittest
from unittest import mock

from app import app
# from apps.bookings.models import Bookings
# from apps.flights.models import Flights
# from .fixtures.add_flights import add_test_bookings


class TestBookingsView(unittest.TestCase):
    def setUp(self):
        """Add some example entries to DB."""
        self.app = app.test_client()
        self.maxDiff = None

    @mock.patch('apps.bookings.views.Flights')
    @mock.patch('apps.bookings.views.Bookings')
    def test_getting_bookings_by_uid(self, mock_bookings, mock_flights):
        """Eg. GET /bookings?uid=4321
        Gets all bookings the UID has and lists them in ascending order
        NB: this endpoint checks for bookings.passenger_id, not bookings.id
        """
        # Mock the database results
        mock_bookings.query.filter_by.return_value.all.return_value = [
            dict(
                bookingId='ABCXYZ',
                flight_number='AY512',
                lastName='Testinen',
                departure='HEL',
            ),
            dict(
                bookingId='ABCXYZ',
                flight_number='AY1024',
                lastName='Testinen',
                departure='SIN',
            ),
            dict(
                bookingId='YYYZXO',
                flight_number='AY128',
                lastName='Testinen',
                departure='HEL',
            ),
        ]
        mock_flights.query.filter_by.return_value = [
            dict(
                departure_date='2018-10-23 11:55:00',
                flight_number='AY1024',
            ),
            dict(
                departure_date='2017-12-12 10:40:00',
                flight_number='AY512',
            ),
            dict(
                departure_date='2015-06-23 21:45:00',
                flight_number='AY128',
            )
        ]
        # mock_flights.query.filter_by.return_value.order_by.return_value.first = [
        #     dict(
        #         flight_number='AY1024',
        #         departure='HEL',
        #         departure_date='2018-10-23 11:45:00'
        #     )
        # ]

        response = self.app.get('/bookings?uid=4321')
        bookings = json.loads(response.get_data().decode())
        self.assertEquals(200, response.status_code)
        self.assertEquals(bookings, [{
            'bookingId': 'ABCXYZ',
            'lastName': 'Testinen',
            'departure': 'HEL',
        }, {
            'bookingId': 'ABCXYZ',
            'lastName': 'Testinen',
            'departure': 'SIN',
        }, {
            'bookingId': 'YYYZXO',
            'lastName': 'Testinen',
            'departure': 'HEL',
        }])
    #
    # def test_getting_passenger_bookings_with_return_flights_by_uid(self):
    #     """Eg. GET /bookings?uid=4321&withReturnFlights=true
    #     Gets all bookings the UID has that also have return flights, in ascending order."""
    #     # NB: this endpoint checks for bookings.passenger_id, not bookings.id
    #     response = self.app.get('/bookings?uid=4321&withReturnFlights=true')
    #     bookings = json.loads(response.get_data().decode())
    #     expected_count = Bookings.query.filter_by(passenger_id=4321).count()
    #     self.assertEquals(200, response.status_code)
    #     self.assertEquals(expected_count, len(bookings))
    #     self.assertEquals(bookings, [{
    #         'bookingId': 'ABCXYZ',
    #         'lastName': 'Test1nen',
    #         'departure': 'HEL',
    #     }, {
    #         # TODO
    #     }])
    #
    # def test_getting_a_booking_by_nonexisting_uid(self):
    #     """Eg. GET /bookings?uid=1111"""
    #     # NB: this endpoint checks for bookings.passenger_id, not bookings.id
    #     response = self.app.get('/bookings?uid=1111')
    #     booking = json.loads(response.get_data().decode())
    #     self.assertEquals(404, response.status_code)
    #     self.assertEquals(booking, {
    #         'success': True,
    #         'message': 'No booking was found for passenger ID 1111',
    #     })
    #
    # def test_getting_a_booking_by_booking_id(self):
    #     """Eg. GET /bookings/ABCXYZ"""
    #     response = self.app.get('/bookings/ABCXYZ')
    #     booking = json.loads(response.get_data().decode())
    #     self.assertEquals(200, response.status_code)
    #     self.assertEquals(booking, {
    #         'id': 'ABCXYZ',
    #         'passenger': {
    #             'firstName': 'Test1',
    #             'lastName': 'Test1nen',
    #             'email': 'test1@example.com',
    #         },
    #         'flights': [{
    #             'departure': 'HEL',
    #             'arrival': 'SIN',
    #             'departureDate': '2018-10-16 23:55:00',
    #             'arrivalDate': '2018-10-17 17:15:00',
    #         }, {
    #             'departure': 'SIN',
    #             'arrival': 'SYD',
    #             'departureDate': '2018-10-17 19:15:00',
    #             'arrivalDate': '2018-10-18 06:15:00',
    #         }]
    #     })
