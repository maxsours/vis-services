from flask import Flask
from views import WordCloud, AuthorNetwork, PaperNetwork
from flask.ext.restful import Api
from flask.ext.discoverer import Discoverer
from flask.ext.consulate import Consul, ConsulConnectionError

def create_app():
    """Application factory"""

    app = Flask(__name__, static_folder=None)
    app.url_map.strict_slashes = False

    Consul(app)  # load_config expects consul to be registered
    load_config(app)

    Discoverer(app)
    api = Api(app)
    api.add_resource(WordCloud, '/word-cloud')
    api.add_resource(AuthorNetwork, '/author-network')
    api.add_resource(PaperNetwork, '/paper-network')
    return app


def load_config(app):
    """
    Loads configuration in the following order:
        1. config.py
        2. local_config.py (ignore failures)
        3. consul (ignore failures)
    :param app: flask.Flask application instance
    :return: None
    """

    app.config.from_pyfile('config.py')

    try:
        app.config.from_pyfile('local_config.py')
    except IOError:
        app.logger.warning("Could not load local_config.py")
    try:
        app.extensions['consul'].apply_remote_config()
    except ConsulConnectionError, e:
        app.logger.warning("Could not apply config from consul: {}".format(e))