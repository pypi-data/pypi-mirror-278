from WMain.WRequests import WSession


class Iedu:
    url_login = "https://cas.jlu.edu.cn/tpass/login?service=https://iedu.jlu.edu.cn/jwapp/sys/emaphome/portal/index.do"
    session: WSession

    def __init__(self, session: WSession):
        self.session = session

    def login(self):
        self.session.post(self.url_login)