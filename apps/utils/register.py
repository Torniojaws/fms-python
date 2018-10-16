import importlib


def register_views(app):
    """Routes for the app will be defined here."""
    api_path = "/"

    from apps.bookings.views import BookingsView
    BookingsView.register(app, route_base='{}/bookings/'.format(api_path))


def register_models(app):
    """The database models for registering them."""
    for model in ['bookings', 'flights']:
        mod = importlib.import_module(
            'apps.{}.models'.format(model)
        )
    return mod
