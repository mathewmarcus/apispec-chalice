def test_single_route_no_docstring_no_path_no_ops(app, spec):
    @app.route('/gists/{gist_id}', methods=['GET'])
    def gist_detail(gist_id):
        pass


    spec.add_path(app=app, view=gist_detail)

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {}


def test_single_route_docstring_no_path_no_ops(app, spec):
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


def test_single_route_no_docstring_path_no_ops(app, spec):
    @app.route('/gists/{gist_id}', methods=['GET'])
    def gist_detail(gist_id):
        pass


    spec.add_path(app=app, path='/gists/{gist_id}', view=gist_detail)

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {}


def test_single_route_no_docstring_no_path_ops(app, spec):
    @app.route('/gists/{gist_id}', methods=['GET'])
    def gist_detail(gist_id):
        pass


    spec.add_path(app=app, view=gist_detail, operations={'delete': {}})

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert 'delete' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {}
    assert spec._paths['/gists/{gist_id}']['delete'] == {}


def test_single_route_docstring_path_no_ops(app, spec):
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


    spec.add_path(app=app, path='/gists/{gist_id}', view=gist_detail)

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


def test_single_route_docstring_no_path_ops(app, spec):
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


    spec.add_path(app=app, view=gist_detail, operations={'delete': {}})

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert 'delete' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}'] == {
        'get': {
            'responses': {
                200: {
                    'schema': {
                        '$ref': '#/definitions/Gist'
                    }
                }
            }
        },
        'delete': {}
    }


def test_single_route_no_docstring_path_ops(app, spec):
    @app.route('/gists/{gist_id}', methods=['GET'])
    def gist_detail(gist_id):
        pass


    spec.add_path(app=app, view=gist_detail, operations={'delete': {}}, path='/gists/{gist_id}')

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert 'delete' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {}
    assert spec._paths['/gists/{gist_id}']['delete'] == {}


def test_single_route_docstring_path_ops(app, spec):
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


    spec.add_path(app=app, view=gist_detail, operations={'delete': {}}, path='/gists/{gist_id}')

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert 'delete' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {
        'responses': {
            200: {
                'schema': {
                    '$ref': '#/definitions/Gist'
                }
            }
        }
    }
    assert spec._paths['/gists/{gist_id}']['delete'] == {}



def test_single_route_multiple_view_functions(app, spec):
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

    @app.route('/gists/{gist_id}', methods=['PUT'])
    def other_gist_detail(gist_id):
        '''
        ---
        put:
            responses:
                204:
                    schema:
                        $ref: '#/definitions/Gist'
        '''
        pass


    spec.add_path(app=app, view=gist_detail)
    spec.add_path(app=app, view=other_gist_detail)

    assert '/gists/{gist_id}' in spec._paths
    assert 'get' in spec._paths['/gists/{gist_id}']
    assert 'put' in spec._paths['/gists/{gist_id}']
    assert spec._paths['/gists/{gist_id}']['get'] == {
        'responses': {
            200: {
                'schema': {
                    '$ref': '#/definitions/Gist'
                }
            }
        }
    }
    assert spec._paths['/gists/{gist_id}']['put'] == {
        'responses': {
            204: {
                'schema': {
                    '$ref': '#/definitions/Gist'
                }
            }
        }
    }
