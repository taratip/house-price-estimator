import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from flask import Flask
from config import Config

from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

# initialize bootstrap
bootstrap = Bootstrap(app)


# logging to a file
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/houseestimator.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('HouseEstimator startup')

from app import routes
