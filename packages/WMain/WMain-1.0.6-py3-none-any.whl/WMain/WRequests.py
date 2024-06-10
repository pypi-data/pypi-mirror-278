
import re
import urllib3
import json
from collections.abc import Iterator
from typing import Union, Optional

import requests
from requests.cookies import RequestsCookieJar
from requests import Response
from requests.utils import dict_from_cookiejar, cookiejar_from_dict

from WMain.WUrl import WUrl
from WMain import WUa
from WMain.WResponse import WResponse

urllib3.disable_warnings()


def encode_resp(resp: Response):
    """

    :param resp: Response返回数据类型
    :return: 编码后的Response
    """
    encode = re.findall("charset=[\"']?([a-z0-9-]*)[\"']?", resp.text)
    if encode:
        resp.encoding = encode[0]
    else:
        resp.encoding = resp.apparent_encoding
    return resp


class WRequestINI:
    headers: Optional[dict]
    timeout: Optional[int]
    proxies: Optional[dict]
    verify: Optional[bool]
    cookies: Optional[RequestsCookieJar]
    files: Optional[dict]

    def __init__(self):
        self.headers = {}
        self.timeout = None
        self.proxies = {}
        self.verify = False
        self.cookies = None
        self.files = {}
        self.set_ua()

    def set_proxy(self, port: Union[int, str], ip: str = "127.0.0.1"):
        self.proxies = {"http": f"{ip}:{port}", "https": f"{ip}:{port}"}

    def set_ua(self, choose="win"):
        if choose.lower() in ["win", "window", "windows"]:
            self.headers["User-Agent"] = WUa.get_random_windows_ua()
        elif choose.lower() == "ios":
            self.headers["User-Agent"] = WUa.get_random_ios_ua()
        elif choose.lower() == "mac":
            self.headers["User-Agent"] = WUa.get_random_mac_ua()
        elif choose.lower() == "android":
            self.headers["User-Agent"] = WUa.get_random_android_ua()
        else:
            self.headers["User-Agent"] = choose

    def get_dic(self) -> dict:
        return {
            "timeout": self.timeout,
            "proxies": self.proxies.copy(),
            "verify": self.verify,
            "cookies": self.cookies,
            "headers": self.headers.copy(),
            "files": self.files.copy(),
        }
    
class WSession:
    session: requests.Session
    ini: WRequestINI

    def __init__(self):
        self.ini = WRequestINI()
        self.session = requests.Session()

    def __dic(self, ini: WRequestINI, **kwargs):
        dic = self.ini.get_dic()
        if ini:
            dic.update(ini.get_dic())
        for key, value in kwargs.items():
            if key not in dic:
                dic[key] = value
            if isinstance(value, dict):
                dic[key].update(value)
            else:
                dic[key] = value
        for key in list(dic.keys()).copy():
            if isinstance(dic[key], Iterator) and not dic[key]:
                del dic[key]
        return dic

    def get(self, url: Union[WUrl, str], ini: WRequestINI = None, **kwargs):
        return WResponse(
            encode_resp(self.session.get(str(url), **self.__dic(ini, **kwargs)))
        )

    def post(
        self,
        url: Union[WUrl, str],
        data=None,
        json=None,
        ini: WRequestINI = None,
        **kwargs,
    ):
        return WResponse(
            encode_resp(
                self.session.post(
                    str(url), data=data, json=json, **self.__dic(ini, **kwargs)
                )
            )
        )

    def save_cookies(self, file):
        with open(file, "w") as f:
            f.write(json.dumps(dict_from_cookiejar(self.session.cookies)))

    def load_cookies(self, file):
        with open(file, "r") as f:
            self.session.cookies = cookiejar_from_dict(json.loads(f.read()))
    
    def load_cookies_str(self, cookies_str: str):
        dic = {}
        for cookie in cookies_str.strip().split(";"):
            key, value = cookie.split("=", 1)
            dic[key] = value
        self.load_cookie_dict(dic)
    
    def load_cookie_dict(self, cookie_dict: dict):
        self.session.cookies = cookiejar_from_dict(cookie_dict)
    
    def load_cookie_editor(self, file):
        """
        load cookies from cookie editor json file from web browser plugins

        Args:
            file (_type_): _description_
        """
        with open(file, "rb") as f:
            cookie_json = json.load(f)
        for cookie in cookie_json:
            cookie_dic = {}
            f = {
                "name": "name",
                "value": "value",
                "expirationDate": "expires",
                "domain": "domain",
            }
            for key, value in cookie.items():
                if key in f:
                    cookie_dic[f[key]] = value
            self.session.cookies.set(**cookie_dic)
