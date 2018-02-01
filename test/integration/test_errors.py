import pytest
from apispec.exceptions import APISpecError


def test_undecorated_view(app, spec):
    def gist_detail(gist_id):
        '''
        ---
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/Gist'
        '''
        pass

    
    with pytest.raises(APISpecError):
        spec.add_path(app=app, view=gist_detail)


def test_wrong_path(app, spec):
    @app.route('/gists/{gist_id}', methods=['GET'])
    def gist_detail(gist_id):
        '''
        ---
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/Gist'
        '''
        pass

    
    with pytest.raises(APISpecError):
        spec.add_path(app=app, view=gist_detail, path='/foo')


def test_no_match_docstring_ops_route_methods(app, spec):
    @app.route('/gists/{gist_id}', methods=['GET'])
    def gist_detail(gist_id):
        '''
        ---
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/Gist'
        delete:
            responses:
                204:
                    schema:
                        $ref: '#/definitions/Empty'

        '''
        pass

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
    assert 'delete' not in spec._paths['/gists/{gist_id}']
