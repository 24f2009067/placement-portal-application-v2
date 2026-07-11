from flask import Flask, request
from flask_cors import CORS
from extensions import db
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager
from models import *
from workers import init_celery, celery
from dotenv import load_dotenv
from init_cache import setup_cache, cache

load_dotenv()

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.student import student_bp
from routes.company import company_bp

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = b'8cg7a8b456b70ef3036e3edc1466d53bc8994a127fb848935118c03ca4e81350'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
jwt = JWTManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement_portal.db"
db.init_app(app)

# celery
init_celery(app)

# caching
setup_cache(app)
@app.before_request
def clearCache():
    if request.method in ["POST", "PUT", "DELETE"]:
        cache.clear()

with app.app_context():
    db.create_all()
    if (User.query.filter(User.email == "admin@ppa.com").first() == None):
        admin = User(email="admin@ppa.com", role="admin")
        admin.set_password("password")

        db.session.add(admin)
        db.session.commit()

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)

if __name__ == "__main__":
    app.run(debug=True)