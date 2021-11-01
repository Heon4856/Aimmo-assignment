from flask import Flask
app = Flask(__name__)

def create_app():
    app = Flask(__name__)

    from views import main_views
    app.register_blueprint(main_views.bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()