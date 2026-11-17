from flask import Flask
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

base_dir = Path(__file__).resolve().parent.parent

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder=str(base_dir / 'templates'), static_folder=str(base_dir / 'static'))
    app.config['SECRET_KEY'] = 'portfolio-demo-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(base_dir / 'portfolio.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .models import Project

    with app.app_context():
        db.create_all()

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
