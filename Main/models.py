from main import app
from flask_sqlalchemy import SQLAlchemy

# flask SQLAlchemy reference documentation
# https://flask-sqlalchemy.palletsprojects.com/en/latest/quickstart/#check-the-sqlalchemy-documentation

# foreign keys documentation
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

# query documentation
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/

# create the app
# app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# create the extension
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # display class object as string
    def __repr__(self):
        return '<User %r>' % self.user_id


class Info(db.Model):
    __tablename__ = 'info'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), unique=True, nullable=False)
    # q1
    # q2
    # q3
    # q etc

    # display class object as string
    def __repr__(self):
        return '<Info %r>' % self.id


# create all tables
db.create_all()
