# coding : utf-8

import json
import urllib
import base64
import configparser
from http import cookiejar
from codecs import BOM_UTF8


def lstrip_bom(str_, bom=BOM_UTF8):
    # remove bom header
    if str_.startswith(bom):
        return str_[len(bom):]
    else:
        return str_


class seuLogin(object):
    """docstring for seuLogin"""

    def __init__(self, username, pwd):
        super(seuLogin, self).__init__()
        self.username = username
        self.password = pwd

    def checkLogin(self):
        url = "http://w.seu.edu.cn/index.php/index/init"
        res = urllib.request.urlopen(url)
        info = res.read()
        # remove bom header
        state_info = json.loads(lstrip_bom(info))
        if state_info['status'] == 1:
            print('Login info:', state_info['info'])
            print('Location:', state_info['logout_location'])
            print('Username:', state_info['logout_username'])
            print('IP:', state_info['logout_ip'])
            return True
        else:
            return False

    # no need cookie
    def postWithCookie(self):
        cookiefile = "cookiefile"
        data = {'username': self.username,
                # 'domain': 'teacher',
                'password': base64.b64encode(self.password.encode()),
                'enablemacauth': 0
                }
        url = "https://w.seu.edu.cn/index.php/index/login"
        req = urllib.request.Request(url)
        data = urllib.parse.urlencode(data).encode()
        # user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
        # headers = {'User-Agent': user_agent}
        # enable cookie
        cookieJar = cookiejar.MozillaCookieJar(cookiefile)
        cookieJar.save()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))
        urllib.request.install_opener(opener)
        response = opener.open(req, data)
        cookieJar.save()
        # req = urllib2.Request(url, data, headers)
        # response = urllib2.urlopen(req)
        the_page = response.read()
        state_info = json.loads(lstrip_bom(the_page.strip('\n'.encode())))
        if state_info['status'] == 1:
            print('Login info:', state_info['info'])
            print('Location:', state_info['logout_location'])
            print('Username:', state_info['logout_username'])
            print('IP:', state_info['logout_ip'])
            return True
        else:
            return False

    def Login(self):
        if not self.checkLogin():
            self.postWithCookie()


if __name__ == "__main__":
    cf = configparser.ConfigParser()
    cf.read("account.conf")
    username = cf.get("account", "username")
    password = cf.get("account", "password")
    # print username, password
    s = seuLogin(username, password)
    s.Login()
