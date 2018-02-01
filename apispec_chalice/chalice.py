# -*- coding: utf-8 -*-
"""Chalice plugin. Includes a path helper that allows you to pass a view
function to `add_path`. Inspects URL rules and view docstrings.

Passing a view function::

    from chalice import Chalice

    app = Chalice(__name__)

    @app.route('/gists/{gist_id}')
    def gist_detail(gist_id):
        '''Gist detail view.
        ---
        x-extension: metadata
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/Gist'
        '''
        return 'detail for gist {}'.format(gist_id)

    spec.add_path(app=app, view=gist_detail)
    print(spec.to_dict()['paths'])
    # {'/gists/{gist_id}': {'get': {'responses': {200: {'schema': {'$ref': '#/definitions/Gist'}}}},
    #                  'x-extension': 'metadata'}}

"""

from apispec.compat import iteritems, iterkeys
from apispec import Path
from apispec.exceptions import APISpecError
from apispec.utils import load_operations_from_docstring


def _route_for_view(current_app, view, path=Path(), operations=set()):
    view_funcs = current_app.routes

    for uri, endpoint in iteritems(view_funcs):
        methods = set()
        for method, route_entry in iteritems(endpoint):
            method = method.lower()
            if route_entry.view_function == view and (not operations or method in operations):
                if path.path and not path.path == uri:
                    break
                else:
                    methods.add(method)
        else:
            if methods:
                return uri, methods

    raise APISpecError('Could not find endpoint for view {0} and path {1}'.format(view, getattr(path, 'path', None)))


def path_from_view(spec, app, view, **kwargs):
    """Path helper that allows passing a Chalice view function."""
    kwarg_ops = kwargs.get('operations')
    kwarg_ops = set() if not kwarg_ops else set(kwarg_ops)

    uri, methods = _route_for_view(app, view, path=kwargs.get('path', Path()), operations=kwarg_ops)
    operations = load_operations_from_docstring(view.__doc__)
    if not operations:
        operations = {}

    # check that the operations in the docstring match those of the actual route decorator
    path = Path(path=uri, operations={method:op for method, op in iteritems(operations) if method in methods})

    # add methods from route decorator that were not in docstring
    for op in methods:
        path.operations.setdefault(op, {})
    
    return path


def setup(spec):
    """Setup for the plugin."""
    spec.register_path_helper(path_from_view)
