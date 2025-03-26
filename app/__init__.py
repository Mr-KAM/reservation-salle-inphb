from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.rooms import rooms
    from app.routes.admin import admin

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(rooms)
    app.register_blueprint(admin)

    # Create database tables
    with app.app_context():
        # db.drop_all()
        db.create_all()
        # Initialize database with default data if needed
        from app.models.user import User
        from app.models.room import Room
        from app.models.reservation import Reservation

        # Check if admin user exists, if not create one
        if not User.query.filter_by(email='admin@example.com').first():
            from werkzeug.security import generate_password_hash
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    return app
