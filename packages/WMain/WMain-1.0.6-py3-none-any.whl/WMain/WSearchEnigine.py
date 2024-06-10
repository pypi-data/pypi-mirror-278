from typing import List, Union
from WMain.WRequests import WSession
from WMain.WUrl import WUrl
import re
from WMain.WResponse import WResponse

TARGET_GLOBAL = "GLOBAL"
TARGET_LOCAL = "LOCAL"
TARGET_URL = "URL"

METHOD_GET = "GET"
METHOD_POST = "POST"

FROM_RESP_XPATH = "xpath"
FROM_RESP_RE = "re_str"


class WCrawlerNoUnionsException(Exception):
    pass


class WCrawlerException(Exception):
    pass


class WCrawlerMethod:

    def __init__(self, method: str, data: dict = None):
        self.method: str = method
        self.data: dict = data


class WGetFromResponse:

    def __init__(self, from_resp_type: str, xpath: str = None, re_str: str = None):
        self.xpath: str = xpath
        self.re_str: str = re_str
        self.from_resp_type: str = from_resp_type

    def get_from(self, response: WResponse):
        if self.from_resp_type == FROM_RESP_XPATH:
            return [
                (
                    elem.strip()
                    if isinstance(elem, str)
                    else elem.xpath("string(.)").strip()
                )
                for elem in response.xpath(self.xpath)
            ]
        elif self.from_resp_type == FROM_RESP_RE:
            return re.findall(self.re_str, response.resp.text)
        else:
            raise WCrawlerException("Invalid from_resp_type, should be xpath or re_str")


class WCrawlerTarget:

    def __init__(
        self,
        get_from_resp: WGetFromResponse,
        target_key: str,
        target_type: str = TARGET_LOCAL,
    ):
        self.get_from_resp: WGetFromResponse = get_from_resp
        self.target_type: str = target_type
        self.target_key: str = target_key


class WCrawlerResults:

    def __init__(self):
        self.global_results = {}
        self.local_results = {}

    def add_global_result(self, key: str, value: list):
        if key in self.global_results:
            self.global_results[key].append(value)
        else:
            self.global_results[key] = [value]

    def add_local_result(self, key: str, value: list):
        if key in self.local_results:
            self.local_results[key].append(value)
        else:
            self.local_results[key] = [value]


class WCrawlerEnigine:

    crawl_unions: List[List[Union[WCrawlerMethod, WCrawlerTarget]]] = []
    results: WCrawlerResults = WCrawlerResults()
    session: WSession = WSession()

    def __init__(self, crawl_url: str):
        """
        data = None,  url = https://www.bjzhts.com/vodcrawl/-------------.html?wd=123     GET    -> HTML
        HTML --xpath data method--> HTMLS and targets
        HTMLS --xpath data method--> HTMLS and targets
        LOOP UNTIL HTMLS is empty

        https://www.bjzhts.com/vodcrawl/-------------.html?wd=123
        GET -> 标题,


        Args:
            crawl_url (str): _description_
            main_url (str, optional): _description_. Defaults to None.
        """
        self.crawl_url: str = crawl_url

    def start(self):
        if not crawl_enigine.crawl_unions:
            raise WCrawlerNoUnionsException("No crawl unions found")
        urls = []
        next_urls = [self.crawl_url]
        for unions in crawl_enigine.crawl_unions:
            urls, next_urls = next_urls, []
            method: WCrawlerMethod = unions[0]
            if not isinstance(method, WCrawlerMethod):
                raise WCrawlerException("Invalid method type, should be WCrawlerMethod")
            for url in urls:
                if method.method == METHOD_GET:
                    resp = self.session.get(url)
                elif method.method == METHOD_POST:
                    resp = self.session.post(url, data=method.data)
                else:
                    raise WCrawlerException("Invalid method, should be GET or POST")

                for target in unions[1:]:
                    targets = target.get_from_resp.get_from(resp)
                    if target.target_type == TARGET_URL:
                        next_urls.extend(
                            [WUrl(url).urljoin(join_url) for join_url in targets]
                        )
                    elif target.target_type == TARGET_GLOBAL:
                        self.results.add_global_result(target.target_key, targets)
                    elif target.target_type == TARGET_LOCAL:
                        self.results.add_local_result(target.target_key, targets)
                    else:
                        raise WCrawlerException(
                            "Invalid target_type, should be URL, GLOBAL or LOCAL"
                        )


# TEST
if __name__ == "__main__":
    crawl_enigine = WCrawlerEnigine(
        "https://www.bjzhts.com/vodsearch/-------------.html?wd=你好"
    )
    crawl_enigine.crawl_unions = [
        [
            WCrawlerMethod(METHOD_GET),
            WCrawlerTarget(
                WGetFromResponse(
                    FROM_RESP_XPATH, '//*[@class="title text-overflow"]/a/@href'
                ),
                None,
                TARGET_URL,
            ),
            WCrawlerTarget(
                WGetFromResponse(FROM_RESP_XPATH, '//*[@class="detail"]/p[1]'), "author"
            ),
            WCrawlerTarget(
                WGetFromResponse(
                    FROM_RESP_XPATH, '//*[@class="title text-overflow"]/a'
                ),
                "title",
            ),
            WCrawlerTarget(
                WGetFromResponse(
                    FROM_RESP_XPATH, '//*[@class="more text-muted pull-right"]'
                ),
                "page_num",
                TARGET_GLOBAL,
            ),
        ],
        [
            WCrawlerMethod(METHOD_GET),
            WCrawlerTarget(
                WGetFromResponse(
                    FROM_RESP_XPATH, '//*[@class="btn btn-primary"]/@href'
                ),
                None,
                TARGET_URL,
            ),
        ],
        [
            WCrawlerMethod(METHOD_GET),
            WCrawlerTarget(
                WGetFromResponse(
                    FROM_RESP_RE,
                    re_str=r"(https:[^\"\']*?index.m3u8)",
                ),
                "m3u8_url",
            ),
        ],
    ]
    crawl_enigine.session.ini.set_proxy(20000)
    crawl_enigine.start()
    print(crawl_enigine.results.local_results)
    print(crawl_enigine.results.global_results)
