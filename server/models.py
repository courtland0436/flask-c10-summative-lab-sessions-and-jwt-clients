from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import Bcrypt

# This helps with naming conventions in the database
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    # Add serialization rules to avoid infinite loops with tasks
    serialize_rules = ('-_password_hash', '-tasks.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    # Relationship: A user has many tasks
    tasks = db.relationship('Task', back_populates='user', cascade='all, delete-orphan')

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        # This hashes the password before saving it
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        # This checks the password during login
        return bcrypt.check_password_hash(self._password_hash, password)

class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'

    serialize_rules = ('-user.tasks',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    importance = db.Column(db.Integer) # Extra field 1
    category = db.Column(db.String)   # Extra field 2
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship: A task belongs to one user
    user = db.relationship('User', back_populates='tasks')