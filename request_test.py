# -*- coding: utf-8 -*-
import json
import random
import string

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

IP = '127.0.0.1'
PORT = 5000

def send_get(url,headers = {'content-type': 'application/json'}):
    """POST请求"""
    r = requests.get(url, headers=headers,
                     auth=HTTPDigestAuth('kakou', 'pingworker'))

    return r

def test_hphm_get():
    hphm = u'粤L54322'
    url = 'http://127.0.0.1:5000/hphm/%s' % hphm
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    print r.status_code
    print r.headers
    print r.text

def test_hphm_post():
    url = 'http://127.0.0.1:5000/hphm'
    headers = {'content-type': 'application/json'}
    data = {'hphm': u'粤L54323'}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print r.status_code
    print r.headers
    print r.text

def test_random_hphm():
    a = random.sample('ABCDEFGHJKLMNPQRSTUVW1234567890',6)
    return string.join(a).replace(' ','')

def test_clxx_post():
    url = 'http://127.0.0.1:5000/clxx'
    headers = {'content-type': 'application/json'}
    data = {'date': '2015-09-01','hphm': u'粤L54324'}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print r.status_code
    print r.headers
    print r.text

def test_clxx_get_by_date():
    url = 'http://127.0.0.1:5000/clxx/2015-09-01'
    headers = {'content-type': 'application/json'}
    #data = {'date': '2015-09-01','hphm': u'粤L54324'}
    r = requests.get(url, headers=headers)
    print r.status_code
    print r.headers
    print r.text

if __name__ == '__main__':  # pragma nocover
    #TestHttpPost()
    #test_hphm_get()
    #test_hphm_post()
    #print test_random_hphm()
    #test_clxx_post()
    test_clxx_get_by_date()
