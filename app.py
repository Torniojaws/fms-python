from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from apps.utils.register import register_views, register_models
from settings.config import CONFIG

app = Flask(__name__)
app.config.from_object(CONFIG)
app.url_map.strict_slashes = False
db = SQLAlchemy(app)

register_models(app)
register_views(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
