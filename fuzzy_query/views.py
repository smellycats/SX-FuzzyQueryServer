# -*- coding: utf-8 -*-
from functools import wraps

import arrow
from flask import g, request, jsonify
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from fuzzy_query import db, app, api, auth, limiter, cache, logger, access_logger
from models import Users, Scope, Hphm7, Hphm12, Clxx
#from help_func import *


def verify_addr(f):
    """IP地址白名单"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not app.config['WHITE_LIST_OPEN'] or request.remote_addr == '127.0.0.1' or request.remote_addr in app.config['WHITE_LIST']:
            pass
        else:
            return {'status': '403.6',
                    'message': u'禁止访问:客户端的 IP 地址被拒绝'}, 403
        return f(*args, **kwargs)
    return decorated_function

@auth.verify_password
def verify_password(username, password):
    if username.lower() == 'admin':
        user = Users.query.filter_by(username='admin').first()
    else:
        return False
    if user:
        return sha256_crypt.verify(password, user.password)
    return False


def verify_token(f):
    """token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Access-Token'):
            return {'status': '401.6', 'message': 'missing token header'}, 401
        token_result = verify_auth_token(request.headers['Access-Token'],
                                         app.config['SECRET_KEY'])
        if not token_result:
            return {'status': '401.7', 'message': 'invalid token'}, 401
        elif token_result == 'expired':
            return {'status': '401.8', 'message': 'token expired'}, 401
        g.uid = token_result['uid']
        g.scope = set(token_result['scope'])

        return f(*args, **kwargs)
    return decorated_function

def verify_scope(f):
    """权限范围验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            scope = '_'.join([request.path[1:], request.method.lower()])
        except Exception as e:
            logger.error(e)
        if 'all' in g.scope or scope in g.scope:
            pass
        else:
            return {'status': 405, 'error': 'Method Not Allowed'}, 405
        return f(*args, **kwargs)
    return decorated_function


class Index(Resource):
    
    def get(self):
        print 'test'
        return {
            'user_url': '%suser{/:user_id}' % (request.url_root),
            'scope_url': '%suser/scope' % (request.url_root),
            'token_url': '%stoken' % (request.url_root),
            'hbcimg_url': '%shbc/img/:date/:hphm/:kkdd' % (request.url_root),
            'hbc_url': '%shbc' % (request.url_root)
            #'hbc_url': 'http://%s:%s/hbc/:jgsj/:hphm/:kkdd' % (request.remote_addr, app.config['PORT'])
        }, 200, {'Cache-Control': 'public, max-age=60, s-maxage=60'}


class User(Resource):
    decorators = [verify_token, limiter.limit("5000/hours")]

    @verify_addr
    @verify_scope
    def get(self, user_id):
        user = Users.query.filter_by(id=user_id, banned=0).first()
        if user:
            return {'id': user.id,
                    'username': user.username,
                    'scope': user.scope,
                    'date_created': str(user.date_created),
                    'date_modified': str(user.date_modified),
                    'banned': user.banned}, 200
        else:
            return {}, 404

    @verify_addr
    @verify_scope
    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('scope', type=unicode, required=True,
                            help='A scope field is require', location='json')
        args = parser.parse_args()

        # 所有权限范围
        all_scope = set()
        for i in Scope.query.all():
            all_scope.add(i.name)
        # 授予的权限范围
        request_scope = set(request.json.get('scope', u'null').split(','))
        # 求交集后的权限
        u_scope = ','.join(all_scope & request_scope)

        db.session.query(Users).filter_by(id=user_id).update({'scope': u_scope, 'date_modified': arrow.now().datetime})
        db.session.commit()

        user = Users.query.filter_by(id=user_id).first()
        app.config['SCOPE_USER'][user.id] = set(user.scope.split(','))

        return {
            'id': user.id,
            'username': user.username,
            'scope': user.scope,
            'date_created': str(user.date_created),
            'date_modified': str(user.date_modified),
            'banned': user.banned
        }, 201


class UserList(Resource):
    decorators = [verify_token, limiter.limit("50/minute")]

    @verify_addr
    @verify_scope
    def post(self):
        if not request.json.get('username', None):
            error = {'resource': 'Token', 'field': 'username',
                     'code': 'missing_field'}
            return {'message': 'Validation Failed', 'errors': error}, 422
        if not request.json.get('password', None):
            error = {'resource': 'Token', 'field': 'username',
                     'code': 'missing_field'}
            return {'message': 'Validation Failed', 'errors': error}, 422

        user = Users.query.filter_by(username=request.json['username'],
                                     banned=0).first()
        if not user:
            password_hash = sha256_crypt.encrypt(request.json['password'],
                                                 rounds=app.config['ROUNDS'])
            # 所有权限范围
            all_scope = set()
            for i in Scope.query.all():
                all_scope.add(i.name)
            # 授予的权限范围
            request_scope = set(request.json.get('scope', u'null').split(','))
            # 求交集后的权限
            u_scope = ','.join(all_scope & request_scope)
            u = Users(username=request.json['username'],
                      password=password_hash, scope=u_scope, banned=0)
            db.session.add(u)
            db.session.commit()
            return {
                'id': u.id,
                'username': u.username,
                'scope': u.scope,
                'date_created': str(u.date_created),
                'date_modified': str(u.date_modified),
                'banned': u.banned
            }, 201
        else:
            return {'message': 'username is already esist'}, 422


class ScopeList(Resource):

    @verify_addr
    @verify_token
    @verify_scope
    def get(self):
        scope = Scope.query.all()
        items = []
        for i in scope:
            items.append(row2dict(i))
        return {'total_count': len(items), 'items': items}, 200


def get_uid():
    g.uid = -1
    g.scope = ''
    try:
        user = Users.query.filter_by(username=request.json.get('username', ''),
                                     banned=0).first()
    except Exception as e:
        logger.error(e)
        raise
    if user:
        if sha256_crypt.verify(request.json.get('password', ''), user.password):
            g.uid = user.id
            g.scope = user.scope
            return str(g.uid)
    return request.remote_addr


class TokenList(Resource):
    decorators = [limiter.limit("5/hour", get_uid)]

    @verify_addr
    def post(self):
        if not request.json.get('username', None):
            error = {'resource': 'Token', 'field': 'username',
                     'code': 'missing_field'}
            return {'message': 'Validation Failed', 'errors': error}, 422
        if not request.json.get('password', None):
            error = {'resource': 'Token', 'field': 'username',
                     'code': 'missing_field'}
            return {'message': 'Validation Failed', 'errors': error}, 422
        if g.uid == -1:
            return {'message': 'username or password error'}, 422
        s = Serializer(app.config['SECRET_KEY'],
                       expires_in=app.config['EXPIRES'])
        token = s.dumps({'uid': g.uid, 'scope': g.scope.split(',')})
        return {
            'uid': g.uid,
            'access_token': token,
            'token_type': 'self',
            'scope': g.scope,
            'expires_in': app.config['EXPIRES']
        }, 201, {'Cache-Control': 'no-store', 'Pragma': 'no-cache'}


#车牌号码分解
def decompose_hphm(hphm):
    if hphm == '' or hphm == '-':
        return None
    p_list = []
    fix_hphm = '%s_' % hphm
    for i in range(len(hphm)):
        p_list.append(fix_hphm[i:i+2])
    return p_list


class HphmApi(Resource):
    decorators = [limiter.exempt]

    @verify_addr
    #@verify_token
    def get(self, hphm):
        try:
            if len(hphm) == 7:
                h = Hphm7.query.filter_by(hphm=hphm).first()
            elif hphm == '' or hphm == '-':
                h = None
            else:
                h = Hphm12.query.filter_by(hphm=hphm).first()
            if h:
                return {'id': h.id, 'hphm': h.hphm}, 200
            else:
                return {}, 404
        except Exception as e:
            logger.error(e)
            raise


class HphmList(Resource):
    decorators = [limiter.exempt]

    @verify_addr
    #@verify_token
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hphm', type=unicode, required=True,
                            help='A hphm field is require', location='json')
        args = parser.parse_args()

        try:
            p_list = decompose_hphm(request.json['hphm'])
            if p_list:
                if len(p_list) == 7:
                    hphm = Hphm7(hphm=request.json['hphm'], p1=p_list[1],
                                 p2=p_list[2], p3=p_list[3], p4=p_list[4],
                                 p5=p_list[5], p6=p_list[6])
                else:
                    hphm = Hphm12(hphm=request.json['hphm'])
                db.session.add(hphm)
                db.session.commit()
                return {'id': hphm.id, 'hphm': hphm.hphm}, 201
            else:
                return {'message': 'Bad Request'}, 400,
                {'Content-Type': 'application/json; charset=utf-8',
                 'Server': app.config['HEADER_SERVER']}
        except Exception as e:
            logger.error(e)
            raise


class ClxxApi(Resource):
    decorators = [limiter.limit("500/hours")]

    @verify_addr
    #@verify_token
    def get(self, date):
        try:
            clxx = Clxx.query.filter_by(date=date).all()
            items = []
            for i in clxx:
                items.append({'id': i.id, 'date': str(i.date), 'hphm': i.hphm})
            return {'total_count': len(items), 'items': items}, 200
        except Exception as e:
            logger.error(e)
            raise

        
class ClxxList(Resource):
    decorators = [limiter.exempt]

    @verify_addr
    #@verify_token
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=unicode, required=True,
                            help='A date field is require', location='json')
        parser.add_argument('hphm', type=unicode, required=True,
                            help='A hphm field is require', location='json')
        args = parser.parse_args()
        try:
            f = Clxx.query.filter_by(date=request.json['date'],
                                     hphm=request.json['hphm']).first()
            if not f:
                clxx = Clxx(date=request.json['date'], hphm=request.json['hphm'])
                db.session.add(clxx)
                db.session.commit()
                return {
                    'id': clxx.id,
                    'date': str(clxx.date),
                    'hphm': clxx.hphm
                }, 201
            else:
                return {'message': 'Hphm in this date in already exist'}, 201
        except Exception as e:
            logger.error(e)
            raise


api.add_resource(Index, '/')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/user')
api.add_resource(ScopeList, '/user/scope')
api.add_resource(TokenList, '/token')
api.add_resource(HphmApi, '/hphm/<string:hphm>')
api.add_resource(HphmList, '/hphm')
api.add_resource(ClxxApi, '/clxx/<string:date>')
api.add_resource(ClxxList, '/clxx')


