"""
云码接口
# 数英汉字类型
# 通用数英1-4位 10110
# 通用数英5-8位 10111
# 通用数英9~11位 10112
# 通用数英12位及以上 10113
# 通用数英1~6位plus 10103
# 定制-数英5位~qcs 9001
# 定制-纯数字4位 193
# 中文类型
# 通用中文字符1~2位 10114
# 通用中文字符 3~5位 10115
# 通用中文字符6~8位 10116
# 通用中文字符9位及以上 10117
# 定制-XX西游苦行中文字符 10107
# 计算类型
# 通用数字计算题 50100
# 通用中文计算题 50101
# 定制-计算题 cni 452
"""
from WMain.WRequests import WSession
import base64

# 配置
W_token = "3GaQwdwSBe0Zwv-XpZ7UXiT1nGHDzhsbn2IzBzDp9os"


class CloudCodeClient:
    """
    云码通用连接
    """

    def __init__(self, token):
        self.url = "http://api.jfbym.com/api/YmServer/customApi"
        self.session = WSession()
        self.session.ini.headers["Content-Type"] = "application/x-www-form-urlencoded"
        self.token = token

    def CommonPost(self, base64_str, type_):
        self.data = {
            "image": base64_str,
            "token": self.token,
            "type": type_
        }
        resp = self.session.post(self.url, data=self.data)
        return resp.resp.json()

    def _Post4LPic_by_base64(self, base64_str):
        return self.CommonPost(base64_str, "10110")

    def _Post4LPic(self, img_file):
        with open(img_file, 'rb') as f:
            return self._Post4LPic_by_base64(
                base64.b64encode(f.read()).decode())


class CloudCode_Api(CloudCodeClient):

    def __init__(self):
        super().__init__(W_token)

    def Post4(self, img_file):
        return self._Post4LPic(img_file)["data"]["data"]

    def Post4_by_base64(self, base64_str):
        return self._Post4LPic_by_base64(base64_str)["data"]["data"]
    
api_cloudcode = CloudCode_Api()

if __name__ == '__main__':
    api = CloudCode_Api()
    print(api.Post4("./test.png"))