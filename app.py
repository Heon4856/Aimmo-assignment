from flask import Flask
from db import initialize_db
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = "secret"

    # jwt
    jwt = JWTManager(app)
    app.config['MONGODB_SETTINGS'] = {'db': ':myapp' ,'host': 'mongodb://127.0.0.1:27017'}

    from views import post_views, auth_views

    app.register_blueprint(post_views.bp)
    app.register_blueprint(auth_views.bp)

    return app


app = create_app()
initialize_db(app)

if __name__ == "__main__":
    app.run()
