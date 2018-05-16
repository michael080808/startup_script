# coding : utf-8

import json
import urllib.request
import configparser
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
            return True
        else:
            return False

    # no need cookie
    def Logout(self):
        url = "http://w.seu.edu.cn/index.php/index/logout"
        res = urllib.request.urlopen(url)
        info = res.read()
        # remove bom header
        state_info = json.loads(lstrip_bom(info))
        print('Login info:', state_info['info'])
        if state_info['status'] == 1:
            return True
        else:
            return False

    def Login(self):
        if self.checkLogin():
            self.Logout()


if __name__ == "__main__":
    cf = configparser.ConfigParser()
    cf.read("account.conf")
    username = cf.get("account", "username")
    password = cf.get("account", "password")
    # print username, password
    s = seuLogin(username, password)
    s.Login()
