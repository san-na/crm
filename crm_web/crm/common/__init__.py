# -*- coding: utf-8 -*-

__author__ = "Junhua.Feng"

from flask import g, Blueprint

Common = Blueprint('Common', __name__)

@Common.before_request
def assign_type():
    g.current_type = 'Common'

# circular dependencies
import crm.common.views
