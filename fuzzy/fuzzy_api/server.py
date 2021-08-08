#!/usr/bin/python3

from fuzzy_api.resources.fuzzy    import controller as Fuzzy
from fuzzy_api.resources.auth     import controller as Authenticate
from flask_restful                import Api
from flasgger                     import Swagger
from flask                        import Flask

import config

# Setup Flask Server
app = Flask(__name__)

# Create an APISpec
template = {
    "swagger": "2.0",
    "info": {
        "title": "Fuzzy server API",
        "description": "API build with swagger and Python",
        "version": "0.0.1",
        "contact": {
            "name": "Lucas Lima, Maria Vitoria",
            "url": "https://adb.md.utfpr.edu.br/",
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]

}

# swagger config
app.config['SWAGGER'] = {
    'title': 'Fuzzy API',
    'uiversion': 3,
    "specs_route": "/api/"
}
swagger = Swagger(app, template=template)
app.config.from_object(config.Config)

api = Api(app)

auth = Authenticate.Auth
fuzzy = Fuzzy.Fuzzy

api.add_resource(auth, '/auth')
api.add_resource(fuzzy, '/fuzzy')

if __name__ == "__main__":
    app.run(debug=True)
