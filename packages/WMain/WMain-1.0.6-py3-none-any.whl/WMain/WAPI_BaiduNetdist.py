import os
from typing import List
from WMain.WBasic import get_timestamp10, get_timestamp13
from WMain.WRequests import WSession
from WMain.WAPI_CloudCode import api_cloudcode
from WMain.WUrl import WUrl
import re
from pprint import pprint


class BaiduNetdiskCaptchaException(Exception):
    pass


class BaiduNetdisk:
    session: WSession = WSession()
    list_url: str = "https://pan.baidu.com/api/list"
    filemanager_url: str = "https://pan.baidu.com/api/filemanager"
    create_url: str = "https://pan.baidu.com/api/create"
    template_variable_url: str = "https://pan.baidu.com/api/gettemplatevariable"
    verify_url: str = "https://pan.baidu.com/share/verify"
    transfer_url: str = "https://pan.baidu.com/share/transfer"

    def __init__(self, cookie_file: str = None, session: WSession = WSession()):
        self.session = session
        if cookie_file is not None:
            self.session.load_cookie_editor(cookie_file)
        self.field = {"bdstoken": None, "token": None}  # 请求需要的域

    def init(self):
        params = {"fields": '["bdstoken","token"]'}
        dic = self.session.get(self.template_variable_url, params=params).resp.json()[
            "result"
        ]
        self.field["token"] = dic["token"]
        self.field["bdstoken"] = dic["bdstoken"]

    def list_dir(self, dir: str):
        resp = self.session.get(self.list_url, params={"dir": dir})
        return [dic["path"] for dic in dict(resp.resp.json())["list"]]

    def del_list(self, file_dir_list: List[str]):
        del_list_str = '["' + '","'.join(file_dir_list) + '"]'
        params = {
            "bdstoken": self.field["bdstoken"],
            "async": len(file_dir_list),
            "onnest": "fail",
            "opera": "delete",
        }
        data = {"filelist": del_list_str}
        resp = self.session.post(self.filemanager_url, params=params, data=data)
        errno = resp.resp.json()["errno"]
        if errno == 0:
            return True
        else:
            return errno

    def create_dir(self, dir, over=False):
        params = {"bdstoken": self.field["bdstoken"]}
        data = {"path": dir, "isdir": "1", "block_list": "[]"}
        if dir not in self.list_dir("/" + "/".join(dir.split("/")[:-1])) or over:
            resp = self.session.post(self.create_url, params=params, data=data)
            if resp.resp.json()["errno"] == 0:
                return {dir: True}
            else:
                return {dir: resp.resp.text}
        else:
            return {dir: "error: file already exist"}

    def verify(self, verify_params, verify_data):
        count = 0
        while 1:
            # 开始请求安全api
            # 百度设计了防盗链, 必须有referer
            resp = self.session.post(
                self.verify_url, params=verify_params, data=verify_data
            )
            error = resp.resp.json()["errno"]
            if error == 0:
                return
            elif error == -62:
                # 保存验证码图片
                with open("captcha.jpeg", "wb+") as f:
                    captcha_url = self.session.get(
                        "https://pan.baidu.com/api/getcaptcha?prod=shareverify"
                    ).json()["vcode_img"]
                    f.write(self.session.get(captcha_url).resp.content)
                vcode_str = captcha_url.split("?")[1]
                if count > 3:
                    raise BaiduNetdiskCaptchaException("验证码识别失败")
                vcode = api_cloudcode.Post4_by_base64("captcha.jpeg")
                verify_params["t"] = get_timestamp10()
                verify_data["vcode"] = vcode
                verify_data["vcode_str"] = vcode_str
                count += 1
            else:
                return False

    def auto_save(self, url, dir="/auto_get", pwd=""):
        resp = self.session.get(url)
        self.session.ini.headers["Referer"] = url
        keyword_list = [
            "分享的文件已经被删除",
            "分享的文件已经被取消",
            "因为涉及侵权、色情、反动、低俗等信息，无法访问",
            "链接错误没找到文件",
            "分享文件已过期",
        ]
        if isinstance(resp, str):
            return "访问的页面不存在"
        for keyword in keyword_list:
            if keyword in resp.resp.text:
                return keyword
        url = resp.resp.url
        url_ = WUrl(url)
        
        url_params = url_.params
        surl = url_[1] if "surl" not in url_params else url_params["surl"][0]
        if "pwd" in url_params and pwd == "":
            pwd = url_params["pwd"]
        verify_params = {
            "t": get_timestamp10(),
            "surl": surl,
            "bdstoken": self.field["bdstoken"],
        }
        verify_data = {"pwd": pwd, "vcode": "", "vcode_str": ""}
        
        if "init" in resp.resp.url:
            self.verify(url, verify_params, verify_data)
        resp = self.session.get(url)
        share_uk = re.findall('share_uk:"([0-9]*?)"', resp.resp.text)[0]
        share_id = re.findall('shareid:"([0-9]*?)"', resp.resp.text)[0]
        fs_id = re.findall('"fs_id":([0-9]*?),', resp.resp.text)[0]
        return self.transfer(dir, share_id, share_uk, fs_id, url)

    def transfer(self, dir, share_id, share_uk, fs_id, url):
        transfer_params = {"shareid": share_id, "from": share_uk, "ondup": "newcopy"}
        transfer_data = {
            "fsidlist": f"[{fs_id}]",
            "path": dir,
        }
        resp = self.session.post(
            self.transfer_url, params=transfer_params, data=transfer_data
        )
        if resp.resp.json()["errno"] == 0:
            result = resp.resp.json()["extra"]["list"][0]
            return f'success save to {result["to"]}'
        else:
            return resp.resp.json()

# share_uk:"1100586214790", shareid:"41767244614"

# TEST
if __name__ == "__main__":
    bd = BaiduNetdisk()
    bd.session.ini.set_proxy(20000)
    bd.session.load_cookies_str("""BIDUPSID=47A4E231E0E46B43AEE15B88EB0AE823; PSTM=1709211960; PANWEB=1; BAIDUID=4096E7D5CA58EBFAFC2E74410A9EABBC:FG=1; BAIDUID_BFESS=4096E7D5CA58EBFAFC2E74410A9EABBC:FG=1; BAIDU_WISE_UID=wapp_1716368905447_284; __bid_n=18df493c7f68432fe6bc36; BDUSS=jdIOW1peHhQVFJIamVhaG1iWmdGQTZIdkRoNTAzdlVEQjJnbWNPWUlpdjIyWFptRVFBQUFBJCQAAAAAAAAAAAEAAACuhdCQMTIzxOPU2jEyMTM4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPZMT2b2TE9mW; BDUSS_BFESS=jdIOW1peHhQVFJIamVhaG1iWmdGQTZIdkRoNTAzdlVEQjJnbWNPWUlpdjIyWFptRVFBQUFBJCQAAAAAAAAAAAEAAACuhdCQMTIzxOPU2jEyMTM4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPZMT2b2TE9mW; STOKEN=7acba8426b0472ce3fc69a9e68dc348d376e9f284465819e526048789190b9f9; H_PS_PSSID=60281_60299_60326; ZFY=twP:BmYDKNHkr00kDqkKdJzWFo3gNd8dZCdkFhe1bhI4:C; csrfToken=ql87CNHX6fAB03Z8x8uXApma; newlogin=1; Hm_lvt_95fc87a381fad8fcb37d76ac51fefcea=1717670376; Hm_lpvt_95fc87a381fad8fcb37d76ac51fefcea=1717670399; BDCLND=HWFxeZYAmgS6Pdkaq0pzAs192frbSB9V; RT="z=1&dm=baidu.com&si=b93349fd-8e95-40c5-a034-7100fc72ee40&ss=lx33p342&sl=4&tt=pb&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1c5ye"; PANPSC=13550028444288601911%3ACU2JWesajwByPfGOomAcr8Wn1hbHg1WZbtDq%2BK%2BOodwOYC6rNtBREiQxbl68m9lcBm6rqQ5QdYLfupBU50mzJd4uFpsf7z4CwhRIQmAoMSKHkrigi2TxuAjHRUw%2FZR6kLvxjdeGWe15rqCNYc2LuOFCHZGOaQdgCY8uG8AM%2BY0Ih6uZoP3DwQ7BnXFvU9LYk9FYxwFKTFsK6Qy05m0yAsDCo8bcT1HMK; ndut_fmt=BA88895C3414E8A6B53FEF9D1AA9BFEA07157017EB6D744973692729B6229016""")
    
    bd.init()
    pprint(bd.list_dir("/"))
    pprint(bd.create_dir("/test_dir"))
