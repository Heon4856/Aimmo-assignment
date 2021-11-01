from flask import Flask
from db import initialize_db


def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {'db': ':myapp'}

    from views import main_views

    app.register_blueprint(main_views.bp)

    return app


app = create_app()
initialize_db(app)

if __name__ == "__main__":
    app.run()
