from flask import Flask
from extensions import db
from routes.main import main
from routes.summary import summary

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(summary)
    
    return app

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app = create_app()
    init_db()
    app.run(debug=True)