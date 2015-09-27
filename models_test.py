# -*- coding: utf-8 -*-
import arrow

from fuzzy_query import db
from fuzzy_query.models import Users, Hphm7, Hphm12, Clxx

def test_scope_get():
    scope = Scope.query.all()
    for i in scope:
        print i.name

def test_user_get():
    user = Users.query.filter_by(username='admin', banned=0).first()
    print user.scope

    
def test_hphm7_get():
    hphm = Hphm7.query.first()
    print hphm

def test_hphm7_add():
    hphm = Hphm7(hphm='粤L12345', p1='L1', p2='12', p3='23', p4='34',
                 p5='45', p6='5_')
    db.session.add(hphm)
    db.session.commit()
    print hphm.id

def test_hphm12_get():
    hphm = Hphm12.query.first()
    print hphm

def test_hphm12_add():
    hphm = Hphm12(hphm='粤L12345')
    db.session.add(hphm)
    db.session.commit()
    print hphm.id

def test_clxx_get():
    clxx = Clxx.query.first()
    print type(clxx.date)

def test_clxx_add():
    clxx = Clxx(date='2015-09-22', hphm='粤L12345')
    db.session.add(clxx)
    db.session.commit()
    print clxx.id


if __name__ == '__main__':
    #hpys_test()
    #hbc_add()
    #test_hphm7_add()
    #test_hphm7_get()
    #test_hphm12_add()
    #test_hphm12_get()
    #test_clxx_add()
    test_clxx_get()


