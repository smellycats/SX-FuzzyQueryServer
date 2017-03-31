# -*- coding: utf-8 -*-
import arrow

from fuzzy_query import db
from fuzzy_query.models import Users, Hphm7, Hphm12, Clxx
from sqlalchemy import or_, not_

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

def test_union():
    h1 = db.session.query(Hphm7.hphm).filter_by(p3='23')
    h2 = db.session.query(Hphm12.hphm).filter_by(hphm=u'粤L12345')
    
    q = h1.union_all(h2).all()
    print len(q)

def test_or_filter():
    h7_dict = {3: Hphm7.p3}
    #tu = (h7_dict[3]=='23',Hphm7.p4=='23')
    #help(or_)
    a = (Hphm7.p3=='23')
    a = a | (Hphm7.p4=='23')
    a = a | (Hphm7.p5=='23')
    #print type(a)
    #print a
    #h1 = db.session.query(Hphm7.hphm).filter(or_(h7_dict[3]=='23',Hphm7.p4=='23'))
    h1 = db.session.query(Hphm7.hphm).filter(Hphm7.hphm.like('粤L123%'))
    h1 = h1.filter(a)
    h2 = db.session.query(Hphm12.hphm).filter(Hphm12.hphm.like('粤L123%'))
    #h1 = db.session.query(Hphm7.hphm).filter(or_(Hphm7.p3=='23'))
    #h1 = h1.filter(or_(Hphm7.p4=='23'))
    h3 = h1.union_all(h2)
    print h3
    q = h3.join(Clxx, anon_1.hphm7_hphm == Clxx.hphm)
    #print q
    q = q.all()
    print q

def test_get_hphms():
    h = Hphm7.query.limit(10000).all()
    for i in h:
        c = Clxx(date='2015-09-28', hphm=i.hphm)
        db.session.add(c)
        db.session.commit()
    print 'done'

def test_join():
    h1 = db.session.query(Hphm7.hphm).join(Clxx, Hphm7.hphm == Clxx.hphm).filter(Hphm7.hphm.like('粤L123%')).filter(Clxx.date>='2015-09-28')
    print h1
    print h1.all()
if __name__ == '__main__':
    #hpys_test()
    #hbc_add()
    #test_hphm7_add()
    #test_hphm7_get()
    #test_hphm12_add()
    #test_hphm12_get()
    #test_clxx_add()
    #test_clxx_get()
    #test_union()
    #test_or_filter()
    #test_get_hphms()
    test_join()


