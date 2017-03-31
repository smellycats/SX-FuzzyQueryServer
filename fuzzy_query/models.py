# -*- coding: utf-8 -*-
import arrow

from fuzzy_query import db


class Users(db.Model):
    """用户"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True)
    password = db.Column(db.String(128))
    scope = db.Column(db.String(128), default='')
    date_created = db.Column(db.DateTime, default=arrow.now().datetime)
    date_modified = db.Column(db.DateTime, default=arrow.now().datetime)
    banned = db.Column(db.Integer, default=0)

    def __init__(self, username, password, scope='', banned=0,
                 date_created=None, date_modified=None):
        self.username = username
        self.password = password
        self.scope = scope
        now = arrow.now().datetime
        if not date_created:
            self.date_created = now
        if not date_modified:
            self.date_modified = now
        self.banned = banned

    def __repr__(self):
        return '<Users %r>' % self.id


class Scope(db.Model):
    """权限范围"""
    __tablename__ = 'scope'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Scope %r>' % self.id


class Hphm7(db.Model):
    """7位车牌号码"""
    __tablename__ = 'hphm7'
    id = db.Column(db.Integer, primary_key=True)
    hphm = db.Column(db.String(7), default='-')
    p1 = db.Column(db.String(2), default='__')
    p2 = db.Column(db.String(2), default='__')
    p3 = db.Column(db.String(2), default='__')
    p4 = db.Column(db.String(2), default='__')
    p5 = db.Column(db.String(2), default='__')
    p6 = db.Column(db.String(2), default='__')

    def __init__(self, hphm, p1='__', p2='__', p3='__', p4='__', p5='__', p6='__'):
        self.hphm = hphm
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6

    def __repr__(self):
        return '<Hphm7 %r>' % self.hphm


class GDHphm7(db.Model):
    """7位车牌号码"""
    __tablename__ = 'gd_hphm7'
    id = db.Column(db.Integer, primary_key=True)
    hphm = db.Column(db.String(7), default='-')
    p1 = db.Column(db.String(2), default='__')
    p2 = db.Column(db.String(2), default='__')
    p3 = db.Column(db.String(2), default='__')
    p4 = db.Column(db.String(2), default='__')
    p5 = db.Column(db.String(2), default='__')
    p6 = db.Column(db.String(2), default='__')

    def __init__(self, hphm, p1='__', p2='__', p3='__', p4='__', p5='__', p6='__'):
        self.hphm = hphm
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6

    def __repr__(self):
        return '<GDHphm7 %r>' % self.hphm


class Hphm12(db.Model):
    """不等于7位车牌号码"""
    __tablename__ = 'hphm12'
    id = db.Column(db.Integer, primary_key=True)
    hphm = db.Column(db.String(12), default='-')

    def __init__(self, hphm):
        self.hphm = hphm

    def __repr__(self):
        return '<Hphm12 %r>' % self.hphm


class Clxx(db.Model):
    """每天的车牌号码"""
    __tablename__ = 'clxx'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    hphm = db.Column(db.String(12), default='-')

    def __init__(self, date, hphm):
        self.date = date
        self.hphm = hphm

    def __repr__(self):
        return '<Clxx %r>' % self.id


