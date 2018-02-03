====================
apispec-chalice
====================
.. image:: https://badge.fury.io/py/apispec-chalice.svg
    :target: http://badge.fury.io/py/apispec-chalice
    :alt: Latest version
.. image:: https://travis-ci.org/mathewmarcus/apispec-chalice.svg?branch=master
    :target: https://travis-ci.org/mathewmarcus/apispec-chalice
    :alt: Travis-CI

`Chalice <https://github.com/aws/chalice>`_ plugin for the `apispec <http://apispec.readthedocs.io/en/latest/index.html>`_ (fka Swagger) generation library.

Installation
============
From PyPi::

    $ pip install apispec-chalice

Example RESTful Application
===========================

.. code-block:: python

    from apispec import APISpec
    from chalice import Chalice
    from marshmallow import Schema, fields
    import apispec_chalice

    # Create an APISpec
    spec = APISpec(
        title='Swagger Petstore',
        version='1.0.0',
        plugins=[
            'apispec_chalice',
            'apispec.ext.marshmallow',
        ],
    )

    # Optional marshmallow support
    class CategorySchema(Schema):
        id = fields.Int()
        name = fields.Str(required=True)

    class PetSchema(Schema):
        category = fields.Nested(CategorySchema, many=True)
        name = fields.Str()

    class ErrorSchema(Schema):
        status_code = fields.Int(required=True)
        message = fields.Str()

    app = Chalice(__name__)

    @app.route('/pets', methods=['GET', 'POST'])
    def pets(gist_id):
        '''
        ---
        get:
            responses:
                200:
                    schema:
		        type: array
			items: PetSchema
		404:
		    schema: ErrorSchema
        post:
            responses:
                201:
                    headers:
                        Location:
                            description: 'URI of new pet'
                            type: string
		400:
		    schema: ErrorSchema
        '''
        pass

    @app.route('/pets/{pet_name}', methods=['GET', 'PUT', 'DELETE'])
    def pet(gist_id):
        '''
        ---
        get:
            responses:
                200:
                    schema: PetSchema
		404:
		    schema: ErrorSchema
        delete:
            responses:
                204:
                    description: 'deleted pet'
		404:
		    schema: ErrorSchema
        put:
            responses:
                204:
                    description: 'deleted pet'
		400:
		    schema: ErrorSchema
        '''
        pass

    # Register entities and paths
    spec.definition('Category', schema=CategorySchema)
    spec.definition('Pet', schema=PetSchema)
    spec.definition('Error', schema=ErrorSchema)
    spec.add_path(app=app, view=pets)
    spec.add_path(app=app, view=pet)

Generated OpenAPI Spec
----------------------

.. code-block:: python

    spec.to_dict()
    #{  
    #   'info':{  
    #      'title':'Swagger Petstore',
    #      'version':'1.0.0'
    #   },
    #   'paths':{  
    #      '/pets':{  
    #         'get':{  
    #            'responses':{  
    #               '200':{  
    #                  'schema':{  
    #                     'type':'array',
    #                     'items':{  
    #                        '$ref':'#/definitions/Pet'
    #                     }
    #                  }
    #               },
    #               '404':{  
    #                  'schema':{  
    #                     '$ref':'#/definitions/Error'
    #                  }
    #               }
    #            }
    #         },
    #         'post':{  
    #            'responses':{  
    #               '201':{  
    #                  'headers':{  
    #                     'Location':{  
    #                        'description':'URI of new pet',
    #                        'type':'string'
    #                     }
    #                  }
    #               },
    #               '400':{  
    #                  'schema':{  
    #                     '$ref':'#/definitions/Error'
    #                  }
    #               }
    #            }
    #         }
    #      },
    #      '/pets/{pet_name}':{  
    #         'get':{  
    #            'responses':{  
    #               '200':{  
    #                  'schema':{  
    #                     '$ref':'#/definitions/Pet'
    #                  }
    #               },
    #               '404':{  
    #                  'schema':{  
    #                     '$ref':'#/definitions/Error'
    #                  }
    #               }
    #            }
    #         },
    #         'delete':{  
    #            'responses':{  
    #               '204':{  
    #                  'description':'deleted pet'
    #               },
    #               '404':{  
    #                  'schema':{  
    #                     '$ref':'#/definitions/Error'
    #                  }
    #               }
    #            }
    #         },
    #         'put':{  
    #            'responses':{  
    #               '204':{  
    #                  'description':'deleted pet'
    #               },
    #               '400':{  
    #                  'schema':{  
    #                     '$ref':'#/definitions/Error'
    #                  }
    #               }
    #            }
    #         }
    #      }
    #   },
    #   'tags':[  
    #
    #   ],
    #   'swagger':'2.0',
    #   'definitions':{  
    #      'Category':{  
    #         'type':'object',
    #         'properties':{  
    #            'name':{  
    #               'type':'string'
    #            },
    #            'id':{  
    #               'type':'integer',
    #               'format':'int32'
    #            }
    #         },
    #         'required':[  
    #            'name'
    #         ]
    #      },
    #      'Pet':{  
    #         'type':'object',
    #         'properties':{  
    #            'name':{  
    #               'type':'string'
    #            },
    #            'category':{  
    #               'type':'array',
    #               'items':{  
    #                  '$ref':'#/definitions/Category'
    #               }
    #            }
    #         }
    #      },
    #      'Error':{  
    #         'type':'object',
    #         'properties':{  
    #            'message':{  
    #               'type':'string'
    #            },
    #            'status_code':{  
    #               'type':'integer',
    #               'format':'int32'
    #            }
    #         },
    #         'required':[  
    #            'status_code'
    #         ]
    #      }
    #   },
    #   'parameters':{  
    #
    #   }
    #}
    
    
License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/mathewmarcus/apispec-chalice/blob/master/LICENSE>`_ file for more details.
