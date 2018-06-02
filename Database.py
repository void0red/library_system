from config import login_manager, app
from flask_security import RoleMixin, UserMixin, SQLAlchemySessionUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

# borrow_users = db.Table('borrow_users',
#                        db.Column('borrow_id', db.Integer(), db.ForeignKey('borrow.id')),
#                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))
    # borrows = db.relationship('Borrow', secondary='borrow_users',
    #                           backref=db.backref('users', lazy='dynamic'))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.Integer, nullable=False)
    max_time = db.Column(db.Integer, nullable=False)


class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)


user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)
db.create_all()
user_datastore.find_or_create_role(name='User')
user_datastore.find_or_create_role(name='Admin')

db.session.commit()
