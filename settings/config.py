def database_uri():
    return 'mysql+pymysql://fmstest:fmstest@localhost:3306/fms?charset=utf8mb4'


class Config(object):
    """The app configuration."""
    SQLALCHEMY_DATABASE_URI = database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


CONFIG = Config
