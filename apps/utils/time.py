def get_iso_format(date):
    """Convert the date (a DateTime object from DB, or NULL) to ISO format YYYY-MM-DD HH:MM:SS."""
    if date:
        return date.strftime('%Y-%m-%d %H:%M:%S')
