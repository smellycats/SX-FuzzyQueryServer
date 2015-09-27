# -*- coding: utf-8 -*-

class Config(object):
    # 密码 string
    SECRET_KEY = 'hellokitty'
    # 主机IP string
    # HOST = '0.0.0.0'
    # 端口 string
    # PORT = '8098'
    # 服务器名称
    HEADER_SERVER = 'SX-FuzzyQueryServer'
    # 加密次数 int
    ROUNDS = 123456
    # token生存周期，默认1小时 int
    EXPIRES = 7200
    # 数据库连接 string
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/fuzzyq'
    # 用户权限范围 dict
    SCOPE_USER = {}
    # 白名单启用 bool
    WHITE_LIST_OPEN = True
    # 白名单列表 set
    WHITE_LIST = set()


class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False


class Testing(Config):
    TESTING = True
