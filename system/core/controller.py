"""
    System Core Controller File

    This is the Core Controller that defines how to load views and load models

    We also have to define a dispatch_request method that helps the controller load a view
"""
from flask import current_app, render_template, redirect, request, session, flash, jsonify
from flask.views import View
import requests

# for python3 a bit kludgey
try:
    from urllib.parse import urlencode #, urlparse
    # from urllib.request import urlopen, Request
    # from urllib.error import HTTPError
except ImportError:
    # from urlparse import urlparse
    from urllib import urlencode
    # from urllib2 import urlopen, Request, HTTPError

import importlib

class Controller(View):
    def __init__(self, action):
        super(Controller, self).__init__()

        self._action = action
        self._app = current_app
        self.models = {}

    def dispatch_request(self, *args, **kwargs):
        action = getattr(self, self._action, None)
        if action is None:
            raise Exception('action', 'Action {0} not found'.format(self._action))
        return action(*args, **kwargs)

    def load_view(self, view_name, **kwargs):
        # TODO: Check that a view exists and add error handling for when a view does not exist
        if 'app' not in kwargs:
            kwargs['app'] = self._app

        return render_template(view_name, **kwargs)

    def load_model(self, model_name):
        model = getattr(importlib.import_module('app.models.'+model_name), model_name)
        self.models[model_name] = model()

__all__ = ['Controller', 'request', 'session', 'redirect', 'flash', 'jsonify','requests', 'urlencode']#setting exactly what should be accebible when this module is called 
