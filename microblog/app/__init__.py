from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import text
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
csrf = CSRFProtect(app)

# with app.app_context():
#     raw_sql = """
#     CREATE TABLE IF NOT EXISTS users3 (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         username VARCHAR(64) NOT NULL,
#         email VARCHAR(120) NOT NULL UNIQUE,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
#     """
#     db.session.execute(text(raw_sql))
#     db.session.commit()

from app import routes, models, errors