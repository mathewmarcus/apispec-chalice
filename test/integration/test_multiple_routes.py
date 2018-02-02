def test_one_route_per_view(app, spec):
    @app.route('/gists', methods=['GET', 'POST'])
    def gists(gist_id):
        '''
        ---
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/ManyGist'
        post:
            responses:
                201:
                    headers:
                        Location:
                            description: 'URI of new gist'
                            type: string
                    schema:
                        $ref: '#/definitions/Empty'
        '''
        pass

    @app.route('/gists/{gist_id}', methods=['GET', 'PUT', 'DELETE'])
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
        put:
            responses:
                204:
                    schema:
                        $ref: '#/definitions/Empty'

        '''
        pass

    spec.add_path(app=app, view=gists)
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
    assert 'delete' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['delete'] == {
        'responses': {
            204: {
                'schema': {
                    '$ref': '#/definitions/Empty'
                }
            }
        }
    }
    assert 'put' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['put'] == {
        'responses': {
            204: {
                'schema': {
                    '$ref': '#/definitions/Empty'
                }
            }
        }
    }

    assert '/gists' in spec._paths
    assert 'get' in spec._paths['/gists']
    assert spec._paths['/gists']['get'] == {
        'responses': {
            200: {
                'schema': {
                    '$ref': '#/definitions/ManyGist'
                }
            }
        }
    }
    assert 'post' in spec._paths['/gists']
    assert spec._paths['/gists']['post'] == {
        'responses': {
            201: {
                'schema': {
                    '$ref': '#/definitions/Empty'
                },
                'headers': {
                    'Location': {
                        'description': 'URI of new gist',
                        'type': 'string'
                    }
                }
            }
        }
    }


def test_multiple_routes_per_view(app, spec):
    @app.route('/gists', methods=['GET', 'POST'])
    @app.route('/foobars', methods=['GET', 'POST'])
    def gists(gist_id):
        '''
        ---
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/ManyGist'
        post:
            responses:
                201:
                    headers:
                        Location:
                            description: 'URI of new gist'
                            type: string
                    schema:
                        $ref: '#/definitions/Empty'
        '''
        pass


    spec.add_path(app=app, view=gists, path='/gists')
    spec.add_path(app=app, view=gists, path='/foobars')

    assert '/gists' in spec._paths
    assert 'get' in spec._paths['/gists']
    assert spec._paths['/gists']['get'] == {
        'responses': {
            200: {
                'schema': {
                    '$ref': '#/definitions/ManyGist'
                }
            }
        }
    }
    assert 'post' in spec._paths['/gists']
    assert spec._paths['/gists']['post'] == {
        'responses': {
            201: {
                'schema': {
                    '$ref': '#/definitions/Empty'
                },
                'headers': {
                    'Location': {
                        'description': 'URI of new gist',
                        'type': 'string'
                    }
                }
            }
        }
    }

    assert '/foobars' in spec._paths
    assert 'get' in spec._paths['/foobars']
    assert spec._paths['/foobars']['get'] == {
        'responses': {
            200: {
                'schema': {
                    '$ref': '#/definitions/ManyGist'
                }
            }
        }
    }
    assert 'post' in spec._paths['/foobars']
    assert spec._paths['/foobars']['post'] == {
        'responses': {
            201: {
                'schema': {
                    '$ref': '#/definitions/Empty'
                },
                'headers': {
                    'Location': {
                        'description': 'URI of new gist',
                        'type': 'string'
                    }
                }
            }
        }
    }
    
