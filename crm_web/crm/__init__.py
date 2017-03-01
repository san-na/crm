# -*- coding: utf-8 -*-

__author__ = "Junhua.Feng"


import logging
import logging.handlers
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_jsglue import JSGlue


from crm import settings

db = None
csrf = CsrfProtect()
login_manager = LoginManager()
login_manager.login_view = 'Common.login'
login_manager.login_message = u'请登录后访问!'
login_manager.login_message_category = "info"
jsglue = JSGlue()


def create_app():
    global db

    app = Flask(__name__)
    app.config.from_object(settings)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


    db = SQLAlchemy(app)
    setup_blueprints(app)
    setup_logger(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    jsglue.init_app(app)

    return app

def setup_blueprints(app):
    ''' init blueprints
    '''
    from crm.common import Common
    app.register_blueprint(Common, url_prefix='')

def setup_logger(app):
    """ init logger of operation.
    """
    log_path = app.config['LOG_PATH']
    handler = logging.handlers.TimedRotatingFileHandler(log_path, when='d',
                                                        interval=1)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
