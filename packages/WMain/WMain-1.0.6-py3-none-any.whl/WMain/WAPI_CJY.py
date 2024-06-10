from hashlib import md5
from WMain.WRequests import WSession


class CJYClient:
    """
    超级鹰的通用接口
    """

    def __init__(self, username, password, soft_id):
        """
        :param username: 用户名
        :param password: 密码
        :param soft_id: 软件id
        """
        self.url = "http://upload.chaojiying.net/Upload/Processing.php"
        self.session = WSession()
        self.param = {
            'user': username,
            'pass2': md5(password.encode('utf8')).hexdigest(),
            'softid': soft_id,
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        data = {
            'codetype': codetype,
        }
        data.update(self.param)
        self.session.ini.files = {'userfile': ('ccc.jpg', im)}
        self.session.ini.files = {'userfile': ('ccc.jpg', im)}
        resp = self.session.post(self.url, data=data)
        return resp.resp.json()


class CJY_API(CJYClient):
    """
    超级鹰的个人接口
    """

    def __init__(self):
        super().__init__('weiyn12138', '13214310112', 'python')

    def get_QR(self, file, key="pic_str", port=None):
        """"
        1902	常见4~6位英文数字	10,12,15
        1101	1位英文数字	10
        1004	1~4位英文数字	10
        1005	1~5位英文数字	12
        1006	1~6位英文数字	15
        1007	1~7位英文数字	17.5
        1008	1~8位英文数字	20
        1009	1~9位英文数字	22.5
        1010	1~10位英文数字	25
        1012	1~12位英文数字	30
        1020	1~20位英文数字	50
        """
        # {'err_no': 0, 'err_str': 'OK', 'pic_id': '1211118160954160003',
        # 'pic_str': '7261', 'md5': '4d6a2292dba6e19bb7ed720ed9c1cf92'}
        im = open(file, 'rb').read()
        if port:
            super().session.ini.set_proxy(port)
        return super().PostPic(im, 1902)[key]

api_cjy = CJY_API()

# TEST
if __name__ == '__main__':
    
    api = CJY_API()
    print(api.get_QR("./test.png"))