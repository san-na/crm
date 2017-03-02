# -*- coding: utf-8 -*-

from crm import db
from datetime import datetime
from datetime import timedelta
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, \
     check_password_hash


class Admin(db.Model, UserMixin):
    '''管理员表
    '''
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),index=True)
    email = db.Column(db.String(200),index=True)
    phone = db.Column(db.String(200))
    password = db.Column(db.String(200))
    status = db.Column(db.String(10), default=1)
    last_login = db.Column(db.DateTime, default=datetime.now())
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)
        self.created = datetime.now()
        self.updated = datetime.now()

    def __repr__(self):
        return '<User %r>' % self.name

    def update(self):
        self.updated = datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Customer(db.Model):
    '''客户表
    '''
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100),index=True)
    phone = db.Column(db.String(100),index=True, default='')
    email = db.Column(db.String(100), default='')
    owner = db.Column(db.String(100))
    customer_details = db.Column(db.String(250), default='')
    status = db.Column(db.String(10), default=1)
    sex = db.Column(db.String(10), default=1)
    addr = db.Column(db.String(250))
    company = db.Column(db.String(200))
    note = db.Column(db.String(250))
    group = db.Column(db.String(200))
    tax_id = db.Column(db.String(100), default='')
    modified_by = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, sex, phone, email, company,
                addr, note, tax_id, owner):
        self.name = name
        self.sex = sex
        self.phone = phone
        self.email = email
        self.addr = addr
        self.note = note
        self.owner = owner
        self.modified_by = owner
        self.tax_id = tax_id
        self.company = company
        self.created = datetime.now()
        self.updated = datetime.now()

    def __repr__(self):
        return '<User %r>' % self.name

    def update(self):
        self.updated = datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Group(db.Model):
    '''存放客户组相关信息
    '''
    __tablename__ = 'customer_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200), default="")
    owner = db.Column(db.String(100))
    modified_by = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, description, owner, modified_by):
        self.name = name
        self.description = description
        self.owner = owner
        self.modified_by = modified_by
        self.created = datetime.now()
        self.updated = datetime.now()

    def update(self):
        self.updated = datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Product(db.Model):
    '''存放产品相关信息
    '''
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200), default="")
    owner = db.Column(db.String(100))
    modified_by = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, description, owner, modified_by):
        self.name = name
        self.description = description
        self.owner = owner
        self.modified_by = modified_by
        self.created = datetime.now()
        self.updated = datetime.now()

    def update(self):
        self.updated = datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Opportunity(db.Model):
    '''存放销售机会相关信息
    '''
    __tablename__ = 'opportunity'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    source = db.Column(db.String(200), default="")
    next_contacts = db.Column(db.String(100))
    next_date = db.Column(db.DateTime, default=datetime.now())
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, source, next_contacts):
        self.name = name
        self.source = source
        self.next_contacts = next_contacts
        self.next_date = datetime.now() + timedelta(days=3)
        self.created = datetime.now()
        self.updated = datetime.now()

    def update(self):
        self.updated = datetime.now()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

db.create_all()
db.session.commit()
