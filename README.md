# fms

Endpoints for fms

## Install

1. Install MariaDB, if you don't have it: `sudo apt install mariadb-server`
1. Create the database and user with grants: `sudo mysql` -> `source settings/setup.sql;`
1. Make sure `make` is available
1. Run ``make install``

## Running the project

1. Run ``make run``
1. In a second console, do eg. ``curl localhost:5000/bookings/123`` or
  ``curl localhost:5000/bookings?uid=456``

## Tests

1. You can run tests with ``make test``
