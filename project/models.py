# models.py
from datetime import datetime

from flask_login import UserMixin

from project import db

machine_adaption_table = db.Table('machine_adaption', db.Model.metadata,
                                  db.Column('machine_id', db.Integer, db.ForeignKey('machine.id')),
                                  db.Column('adaption_id', db.Integer, db.ForeignKey('adaption.id')))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Machine(db.Model):
    __tablename__ = 'machine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), )
    description = db.Column(db.Text)
    adaption = db.relationship("Adaption", secondary=machine_adaption_table)

    def __repr__(self):
        return '%r' % (self.name)


class Adaption(db.Model):
    __tablename__ = 'adaption'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return '%r' % (self.name)


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return '%r' % (self.name)


class Offers(db.Model):
    __tablename__ = 'offers'
    id = db.Column("id", db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, server_default=db.func.now())

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship("Customer")

    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'))
    machine = db.relationship("Machine")

    def __repr__(self):
        return '%r' % (self.price)



class Storage(db.Model):
    __tablename__ = 'storage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))
    type = db.Column(db.Unicode(3))
    create_date = db.Column(db.DateTime, default=datetime.now)
