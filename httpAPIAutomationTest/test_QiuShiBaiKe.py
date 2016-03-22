# -*- coding: utf-8 -*-

import sys
import unittest

import json
import datetime
import time
import hashlib
import requests
import config
# import pytest
from requests.adapters import HTTPAdapter
from requests.auth import HTTPDigestAuth, _basic_auth_str
from requests.auth import HTTPBasicAuth
from requests.compat import (
    Morsel, cookielib, getproxies, str, urljoin, urlparse, is_py3, builtin_str)
from requests.cookies import cookiejar_from_dict, morsel_to_cookie
from requests.exceptions import (ConnectionError, ConnectTimeout,
                                 InvalidSchema, InvalidURL, MissingSchema,
                                 ReadTimeout, Timeout, RetryError)
from requests.models import PreparedRequest
from requests.structures import CaseInsensitiveDict
from requests.sessions import SessionRedirectMixin
from requests.models import urlencode
from requests.hooks import default_hooks

import HTMLTestRunner

if config.g_bTestServer:
    print 'Connect to the test server!'
    URL_API = 'http://119.29.63.205'
    HOST_API = 'm2.qiushibaike.com'
else:
    print 'Connect to the production server!'
    URL_API = 'http://m2.qiushibaike.com'
    HOST_API = None

HOST_INSP = 'http://insp.qiushibaike.com'
HOST_WEB = 'http://www.qiushibaike.com'
PORT = '1000'

# ----------------------------------------------------------------------
def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')
# ----------------------------------------------------------------------

# Test cases to drive the HTMLTestRunner

class Register(unittest.TestCase):
    """Register
    """
    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)

    def test_Register(self):
        pass
    pass

class LoginLogout(unittest.TestCase):
    """Login and Logout
    """

    login_info = []

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)

    def test_Login(self):
        """用户登录时调用的接口
        请求方式: http POST
        示例：http:// m2.qiushibaike.com/user/signin

        用户登录时还要调用另外一个接口,存入用户相关信息
            请求方式: http POST
            示例：http:// push.qiushibaike.com/push
        """
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            # 'Content-Length': '316',
            'Content-Type': 'multipart/form-data',

            'Charsert': 'UTF-8',
            'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            # 'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            'Connection': 'keep-alive',
            'Host': HOST_API,
            # 'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {'login': 'roy.burns@163.com',
                'pass': '123123'
                }

        # r = requests.get(HOST + '/user/signin', data=data, headers=headers)
        # r = requests.post(URL_API + '/user/signin', auth=('roy.burns@163.com', '123123qb'), headers=headers)
        r = requests.post(URL_API + '/user/signin', json=data, headers=headers)

        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        assert r.status_code == 200 or r.status_code == 202
        LoginLogout.login_info = r.json()
        assert LoginLogout.login_info['err'] == 0
        print LoginLogout.login_info['token']

        #
        headers['Qbtoken'] = LoginLogout.login_info['token']
        data = {'token': LoginLogout.login_info['token'],
                'action': 'login'
                }
        r = requests.post('http://push.qiushibaike.com/push', json=data, headers=headers)

        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        assert r.status_code == 200 or r.status_code == 202
        responds = r.json()
        assert responds['err'] == 0
        pass

    def test_Login_thirdpart(self):
        """用户登录时调用的接口
        请求方式: http POST
        示例：http:// m2.qiushibaike.com/user/signin

        用户登录时还要调用另外一个接口,存入用户相关信息
            请求方式: http POST
            示例：http:// push.qiushibaike.com/push
        """
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            # 'Content-Length': '316',
            'Content-Type': 'multipart/form-data',

            'Charsert': 'UTF-8',
            'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            # 'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            'Connection': 'keep-alive',
            'Host': HOST_API,
            # 'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {'sns': 'qq', #第三方平台（’wx’,’qq’,’wb’)
                'token': ''     #第三方token
                }

        # r = requests.get(HOST + '/user/signin', data=data, headers=headers)
        # r = requests.post(URL_API + '/user/signin', auth=('roy.burns@163.com', '123123qb'), headers=headers)
        r = requests.post(URL_API + '/user/v2/signin', json=data, headers=headers)

        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        assert r.status_code == 200 or r.status_code == 202
        LoginLogout.login_info = r.json()
        assert LoginLogout.login_info['err'] == 0
        print LoginLogout.login_info['token']

        #
        headers['Qbtoken'] = LoginLogout.login_info['token']
        data = {'token': LoginLogout.login_info['token'],
                'action': 'login'
                }
        r = requests.post('http://push.qiushibaike.com/push', json=data, headers=headers)

        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        assert r.status_code == 200 or r.status_code == 202
        responds = r.json()
        assert responds['err'] == 0
        pass

    def test_Logout(self):
        """用户登录时调用的接口
        请求方式: http POST
        示例：http:// m2.qiushibaike.com/user/signin

        用户登录时还要调用另外一个接口,存入用户相关信息
            请求方式: http POST
            示例：http:// push.qiushibaike.com/push
        """
        assert LoginLogout.login_info

        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            # 'Content-Length': '316',
            'Content-Type': 'multipart/form-data',

            'Charsert': 'UTF-8',
            'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            # 'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            'Connection': 'keep-alive',
            'Host': HOST_API,
            # 'Content-Type': 'application/x-www-form-urlencoded',
        }

        headers['Qbtoken'] = LoginLogout.login_info['token']
        data = {'token': LoginLogout.login_info['token'],
                'action': 'logout',
                }
        r = requests.post('http://push.qiushibaike.com/push', json=data, headers=headers)

        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        assert r.status_code == 200 or r.status_code == 202
        responds = r.json()
        assert responds['err'] == 0
        pass

    pass

class Article(unittest.TestCase):
    """ Article
    """

    # store the article info, return from server
    article = []
    comment = []

    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        # self.article = []
        # self.comment = []

    def test_CreateArticle(self):
        """用户发表一个帖子时调用的接口
        """

        headers = {
            # 'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            # 'Content-Length': '316',
            # 'Content-Type': 'multipart/form-data;boundary=e4f30696-3edc-4fd4-a457-98967c9e972c',

            # 'Charsert': 'UTF-8',
            # 'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            # 'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            # 'Connection': 'keep-alive',
            # 'Host': HOST_API,
        }
        # this params can be ignore.
        params = {
            'imgsrc': '-1',
            'from_topic': '0',
        }
        m = hashlib.md5()
        m.update('%s' % (datetime.datetime.now()))
        mv = m.hexdigest()
        content = '%s...' % mv
        data = {
            "allow_comment": True,
            "anonymous": False,
            "city": "深圳市",
            'content': content,
            "display": 1,
            "district": "南山区",
            'image_height': 0,
            # 'image_type': ,
            'image_width': 0,
            "latitude": 22.5399,
            "longitude": 113.9571,
            "screen_height": 1920,
            "screen_width": 1080,
        }

        # Content-Disposition: form-data; name=json
        # Content-Type: text/plain; charset=unicode
        # Content-Transfer-Encoding: 8bit
        boundary = 'e4f30696-3edc-4fd4-a457-98967c9e972c'
        data2 = []
        data2.append('--%s' % boundary)
        data2.append('Content-Disposition: form-data; name=json\n')
        data2.append('Content-Type: text/plain; charset=unicode\n')
        data2.append('Content-Transfer-Encoding: 8bit\r\n')
        data2.append(json.dumps(data) + '\r\n')
        data2.append('--%s' % boundary)

        # r = requests.post(HOST + '/article/create?imgsrc=-1&from_topic=0', data=data, headers=headers)
        # r = requests.post(URL_API + '/article/create', data='\r\n'.join(data2), params=params, headers=headers)
        # data=json.dumps({'json': data})
        # r = requests.post(URL_API + '/article/create', data, params=params, headers=headers)
        # files = {'json': ('', json.dumps(data))}
        # r = requests.post(URL_API + '/article/create', files, headers=headers)
        session = requests.Session()
        files = {'json': ('', json.dumps(data))}
        r = session.post(URL_API + '/article/create', files=files, headers=headers)
        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        assert r.status_code == 200 or r.status_code == 202

        Article.article = r.json()
        assert Article.article
        assert Article.article['err'] == 0
        assert Article.article['article']
        print Article.article['article']['id']
        pass

    def test_Review(self):
        """审
        POST /review
        """

        # assert self.article
        # assert self.article['article']
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            # 'Content-Length': '316',
            'Content-Type': 'application/x-www-form-urlencoded',

            'Charsert': 'UTF-8',
            'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            'Connection': 'keep-alive',
            'Host': HOST_API,
        }
        data = {
            # 'id': self.article['article']['id'],
            'id': '110974611',
            'ret': '1',
        }

        # send requests
        # article_id = self.article['article']['id']
        # article_id = 110935816
        r = requests.post(HOST_INSP + '/review', json=data, headers=headers)
        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        # check
        assert r.status_code == 200 or r.status_code == 202

        self.comment = r.json()
        assert self.comment
        assert self.comment['err'] == 0
        print self.comment['id']

        pass

    def test_CreateComment(self):
        """用户对一个帖子发表评论时调用的接口
        请求方式: http POST
        示例：http://.../article/(\d+:帖子id)/comment/create
        """

        # assert Article.article
        # assert Article.article['article']
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            # 'Content-Length': '316',
            'Content-Type': 'application/x-www-form-urlencoded',

            'Charsert': 'UTF-8',
            'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            'Connection': 'keep-alive',
            'Host': HOST_API,
        }
        m = hashlib.md5()
        m.update('%s' % (datetime.datetime.now()))
        mv = m.hexdigest()
        data = {
            "anonymous": False,
            # "content": '评论%s' % (datetime.datetime.now()),
            "content": '%s' % mv,
        }

        # send requests
        # article_id = Article.article['article']['id']
        # article_id = 107324517
        # article_id = 111071020
        article_id = 112096060
        r = requests.post(URL_API + '/article/%d/comment/create' % article_id, json=data, headers=headers)
        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        # check
        assert r.status_code == 200 or r.status_code == 202

        Article.comment = r.json()
        assert Article.comment
        assert Article.comment['err'] == 0
        # assert Article.comment['id'] != '6152886'
        print Article.comment['id']
        pass

    def test_GetArticle(self):
        """获取帖子内容
        GET /article/110928060
        """

        # assert self.article
        # assert self.article['article']
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            'Charsert': 'UTF-8',
            'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            'Connection': 'keep-alive',
            'Host': HOST_API,
        }

        # send requests
        # article_id = self.article['article']['id']
        article_id = 110930848
        r = requests.get(URL_API + '/article/%d' % article_id, headers=headers)
        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        # check
        assert r.status_code == 200 or r.status_code == 202

        self.respond = r.json()
        assert self.respond
        assert self.respond['err'] == 0
        print self.respond['article']['id']

        pass

    def test_GetComments(self):
        """获取帖子的评论
        GET /article/110928060/comments
        """

        assert Article.article
        assert Article.article['article']
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            'Charsert': 'UTF-8',
            'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            'Connection': 'keep-alive',
            'Host': HOST_API,
        }

        # send requests
        article_id = Article.article['article']['id']
        # article_id = 110930848
        r = requests.get(HOST_INSP + '/article/%d/comments' % article_id, headers=headers)
        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        # check
        assert r.status_code == 200 or r.status_code == 202

        self.respond = r.json()
        assert self.respond
        assert self.respond['err'] == 0
        print self.respond['count']

        pass

    def test_DeleteComment(self):
        """用户删除自己发表的评论时调用的接口
        请求方式: http POST
        示例：http://.../user/comment/delete/
        311760940
        """

        # assert self.comment
        # assert Article.article
        # assert Article.article['article']
        assert Article.comment
        # assert Article.comment['id'] != '6152886'
        if Article.comment['id'] == '6152886':
            return 
            pass
        time.sleep(2)
        # assert self.article['article']
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            # 'Content-Length': '316',
            'Content-Type': 'application/x-www-form-urlencoded',

            'Charsert': 'UTF-8',
            'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            'Connection': 'keep-alive',
            'Host': HOST_API,
        }
        data = {
            # "user_id": Article.article['article']['user']['id'],
            "user_id": '%d' % 28781010,
            "comment_id": Article.comment['id'],
            # "comment_id": '%d' % 312730070,
            # "article_id": Article.article['article']['id'],
            # "article_id": '%d' % 110935500,
            # "article_id": '%d' % 111071020,
            "article_id": '%d' % 112096060,
        }

        # send requests
        r = requests.post(URL_API + '/user/comment/delete/', json=data, headers=headers)
        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        # check
        assert r.status_code == 200 or r.status_code == 202

        self.respond = r.json()
        assert self.respond
        assert self.respond['err'] == 0
        pass

    def test_DeleteArticle(self):
        """用户删除自己发表的帖子调用的接口
        请求方式: http POST
        示例：http://.../article/(\d+:帖子id)/del
        """

        assert Article.article
        headers = {
            'Accept-Encoding': 'gzip',
            'User-Agent': 'qiushibalke_7.1.1_WIFI_auto_6',

            # 'Content-Length': '316',
            'Content-Type': 'application/x-www-form-urlencoded',

            'Charsert': 'UTF-8',
            'Deviceidinfo': '{"DEVICEID":"864587026299967","RANDOM":"","ANDROID_ID":"3f074efcb854e4a9","SIMNO":"89860080191455904417","IMSI":"460007290288560","SERIAL":"16a75f38","MAC":"c0:ee:fb:05:1c:36","SDK_INT":18}',
            'Model': 'ONEPLUS/A0001/A0001:4.3/JLS36C/1390465867:user/release-keys',
            'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
            'Source': 'android_7.1.1',
            'Uuid': 'IMEI_c869b03183e993a76b3b1dbd5c83dd00',

            'Connection': 'keep-alive',
            'Host': HOST_API,
        }

        # send requests
        article_id = Article.article['article']['id']
        # article_id = 110928418
        r = requests.post(URL_API + '/article/%d/del' % article_id, headers=headers)
        print(r.status_code)
        print(r.reason)
        print(r.headers['content-type'])
        print(r.text)

        # check
        assert r.status_code == 200 or r.status_code == 202

        self.respond = r.json()
        assert self.respond
        assert self.respond['err'] == 0

        pass

    pass

# ------------------------------------------------------------------------
# This is the main test on HTMLTestRunner

class QiuShiBaiKe(unittest.TestCase):

    def test_main(self):

        # suite of TestCases
        # suite = unittest.TestSuite()
        # suite.addTest(InequalityTest("testNotEqual"))
        # suite.addTest(InequalityTest("testEqual"))
        # runner = unittest.TextTestRunner()
        # runner.run(suite)
        self.suite = unittest.TestSuite()
        # self.suite.addTests([
        #     # unittest.defaultTestLoader.loadTestsFromTestCase(Register),
        #     # unittest.defaultTestLoader.loadTestsFromTestCase(LoginLogout),
        #     unittest.defaultTestLoader.loadTestsFromTestCase(Article),
        #     ])

        # LoginLogout
        # self.suite.addTests([
        #     LoginLogout('test_Login'),
        #     LoginLogout('test_Logout'),
        # ])

        # Article
        self.suite.addTests([
            LoginLogout('test_Login'),
            Article('test_CreateArticle'),
            Article('test_CreateComment'),
            # Article('test_GetArticle'),
            # Article('test_GetComments'),
            Article('test_DeleteComment'),
            Article('test_DeleteArticle'),
            LoginLogout('test_Logout'),
        ])

        # Invoke TestRunner
        # buf = StringIO.StringIO()
        fp = file('report_qiushibaike.html', 'wb')
        # runner = unittest.TextTestRunner(buf)       #DEBUG: this is the unittest baseline
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title='[Qiushibaike http server api test]',
            description='This report output by HTMLTestRunner.'
            )
        runner.run(self.suite)

##############################################################################
# Executing this module from the command line
##############################################################################

import unittest

if __name__ == "__main__":
    if len(sys.argv) > 1:
        argv = sys.argv
    else:
        argv = ['test_QiuShiBaiKe.py', 'QiuShiBaiKe']
    
    # HTTPBIN = os.environ.get('HTTPBIN_UR', 'http://httpbin.org/')
    # print(HTTPBIN)
    # h = requests.head(HOST)
    # print(h.reason)
    # print(h.headers)

    unittest.main(argv=argv)
    # Testing HTMLTestRunner with HTMLTestRunner would work. But instead
    # we will use standard library's TextTestRunner to reduce the nesting
    # that may confuse people.
    #HTMLTestRunner.main(argv=argv)
