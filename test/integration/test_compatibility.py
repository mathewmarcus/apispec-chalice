from marshmallow import fields, Schema
from apispec import APISpec


def test_single_route_no_app_no_view(spec):
    spec.add_path(path='/gists/{gist_id}', operations={'get': {}})

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {}


def test_single_route_no_view(app, spec):
    spec.add_path(app=app, path='/gists/{gist_id}', operations={'get': {}})

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {}


def test_single_route_no_app(app, spec):
    @app.route('/gists/{gist_id}', methods=['GET'])
    def gist_detail(gist_id):
        pass


    spec.add_path(view=gist_detail, path='/gists/{gist_id}', operations={'get': {}})

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {}


def test_marshmallow_integration(app):
    spec = APISpec(
        title='Swagger Petstore',
        version='1.0.0',
        plugins=[
            'apispec_chalice',
            'apispec.ext.marshmallow'
        ],
    )
    @app.route('/gists/{gist_id}', methods=['GET'])
    def gist_detail(gist_id):
        '''
        ---
        get:
            responses:
                200:
                    schema: GistSchema
        '''
        pass

    class GistSchema(Schema):
        id = fields.Int()
        name = fields.Str(required=True)

    spec.definition('Gist', schema=GistSchema)
    spec.add_path(app=app, view=gist_detail)

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {
        'responses': {
            200: {
                'schema': {
                    '$ref': '#/definitions/Gist'
                }
            }
        }
    }

