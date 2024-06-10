from Crypto.Cipher import AES
from typing import List, Dict, Union
from WMain.WRequests import WSession
from WMain.WUrl import WUrl
from WMain.WThread import WMultiThread, WLock
from Crypto.Util.Padding import pad
from WMain.WFile import create_path
import os

EXT_KEY = "#EXT-X-KEY"
EXT_INF = "#EXTINF"
EXT_VIDEO = "#EXT-X-VIDEO"
EXT_DISCONTINUITY = "EXT-X-DISCONTINUITY"
EXT_END = "#EXT-X-ENDLIST"
EXT_SEQUENCE = "#EXT-X-MEDIA-SEQUENCE"

METHOD_OVER = "OVER"
METHOD_CHECK = "CHECK"

STATUS_READY = "READY"
STATUS_DOWNLOADING = "DOWNLOADING"
STATUS_MERGE = "MERGE"
STATUS_FINISH = "FINISH"
STATUS_ERROR = "ERROR"

thread_num = 16


def aes_decode(data, key: bytes, iv: bytes = 0):
    """AES解密
    :param iv:
    :param key:  密钥 16.32 一般16的倍数
    :param data:  要解密的数据
    :return:  处理好的数据
    """
    data = pad(data, 16)
    cryptor = AES.new(key, AES.MODE_CBC, IV=bytes(iv))
    plain_text = cryptor.decrypt(data)
    return plain_text.rstrip(b"\0")


def attrs_to_dic(attrs: List[str]) -> Dict[str, str]:
    dic = {}
    for i in attrs:
        if "=" in i:
            key, value = i.split("=", 1)
            dic[key] = value.strip('"')
    return dic


class M3U8Union:
    """
    m3u8的最小单位, 一行的数据
    """

    basic_tag: str = "#EXT-X-VIDEO"
    attrs: List[str] = []

    def __init__(self, m3u8_line: str):
        m3u8_line = m3u8_line.strip()

        if m3u8_line.startswith("#"):
            if ":" not in m3u8_line:
                m3u8_line += ":"
            self.basic_tag, attrs_ = m3u8_line.split(":")
        else:
            attrs_ = m3u8_line
        self.attrs = [attr.strip() for attr in attrs_.split(",") if attr.strip()]


class M3U8VideoList:
    method: Union[None, str]
    key_url: Union[None, str]
    key: Union[None, bytes]
    url_list: List[str]
    iv: Union[None, bytes]
    
    def __init__(self):
        self.method = None
        self.key_url = None
        self.key = None
        self.url_list = []
        self.iv = None

class M3U8Resource:
    """
    M3U8中不含#的资源, 配置函数Downloader通过Session实现资源的下载
    里面存有


    """

    unions: List[M3U8Union]
    caches: Dict[str, List[List[str]]]
    all_time: int
    m3u8_text: str
    url: WUrl
    session: WSession
    
    def __init__(self, m3u8_url: str):
        self.unions = []
        self.caches = {}
        self.m3u8_text = ""
        self.all_time = 0
        self.url = WUrl(m3u8_url)
        self.session = WSession()

    def __getitem__(self, item) -> List[List[str]]:
        return self.get_tag(item)

    def set_session(self, session: WSession):
        self.session = session

    def set_m3u8_text_by_session(self, session: WSession = None):
        if not session:
            m3u8_text = self.session.get(self.url).resp.text
        else:
            self.session = session
            m3u8_text = session.get(self.url).resp.text
        self._m3u8_parse(m3u8_text)

    def set_m3u8_text_by_str(self, m3u8_text: str = None):
        self._m3u8_parse(m3u8_text)

    def set_m3u8_text_by_file(self, m3u8_file: str = None):
        with open(m3u8_file, "r") as f:
            m3u8_text = f.read()
        self._m3u8_parse(m3u8_text)

    def _m3u8_parse(self, m3u8_text: str):
        self.m3u8_text = m3u8_text
        self.caches.clear()
        self.unions = [
            M3U8Union(line) for line in m3u8_text.split("\n") if line.strip()
        ]
        self.all_time = sum([float(attrs[0]) for attrs in self[EXT_INF]])

    def get_tag(self, tag) -> List[List[str]]:
        """

        :param tag: 标签
        :return:  返回所有的属性列表
        """
        if tag in self.caches.keys():
            return self.caches[tag]
        self.caches[tag] = []
        for i in self.unions:
            if i.basic_tag == tag:
                self.caches[tag].append(i.attrs)
        return self.caches[tag]

    def to_downloader(self, filepath: str, filename: str):
        return M3U8Downloader(self, filepath, filename)

    def get_video_list(self) -> List[M3U8VideoList]:
        r = []
        sequence = "0"
        video_list = M3U8VideoList()
        for i in self.unions:
            if i.basic_tag == EXT_KEY:
                attrs = attrs_to_dic(i.attrs)
                if "METHOD" in attrs:
                    video_list.method = attrs["METHOD"]
                if "URI" in attrs:
                    video_list.key_url = self.url.urljoin(attrs["URI"])
                if "IV" in attrs:
                    video_list.IV = (
                        attrs["IV"].replace("0x", "").rjust(16, "0")[:16].encode()
                    )
                else:
                    video_list.IV = sequence
            elif i.basic_tag == EXT_VIDEO:
                video_list.url_list.append(self.url.urljoin(i.attrs[0]))
            elif i.basic_tag == EXT_DISCONTINUITY:
                r.append(video_list)
                video_list = M3U8VideoList()
                sequence = "0"
            elif i.basic_tag == EXT_END:
                r.append(video_list)
                video_list = M3U8VideoList()
                sequence = "0"
            elif i.basic_tag == EXT_SEQUENCE:
                sequence = i.attrs[0]
        return r

    def save(self, file: str):
        with open(file, "w") as f:
            f.write(self.m3u8_text)

class M3U8DownloadTask:
    url: WUrl
    key: Union[None, bytes]
    iv: Union[None, bytes]
    session: WSession
    file: str

    def __init__(self, url, key, iv, session, file):
        self.url = url
        self.key = key
        self.iv = iv
        self.session = session
        self.file = file

    def get_data(self, mothed: str):
        if (
            mothed == METHOD_CHECK
            and os.path.exists(self.file)
            and os.path.getsize(self.file) > 0
        ):
            return
        while 1:
            try:
                data = self.session.get(self.url).resp.content
                break
            except Exception:
                continue
        if self.key:
            data = aes_decode(data, self.key, self.iv)
        with open(self.file, "wb") as f:
            f.write(data)


class M3U8Downloader:
    mothed: str
    video_url_list: List[M3U8VideoList]
    res: M3U8Resource
    tasks: List[M3U8DownloadTask]
    task_finished_num: int
    task_all_num: int
    thread: WMultiThread
    progress: float
    _merge_ok: bool
    status: str
    _file: str
    _f_tspath: str
    
    def __init__(self, m3u8_res: M3U8Resource, filepath: str, filename: str):
        self.video_url_list = []
        self.tasks = []
        self.task_finished_num = 0
        self.task_all_num = 0
        self.thread = WMultiThread(thread_num)
        self.progress = 0
        self._merge_ok = False
        self.status = STATUS_READY
        self.res = m3u8_res
        self.mothed = METHOD_CHECK
        
        filepath = filepath.rstrip("/") + "/"
        create_path(filepath)
        create_path(filepath + "ts/")
        self._file = filepath + filename
        self._f_tspath = filepath + "ts/"
        open(self._file, "wb").close()
        self.flush_tasks()

    def flush_tasks(self):
        self.video_url_list = self.res.get_video_list()
        for i in self.video_url_list:
            if i.key_url:
                i.key = self.res.session.get(i.key_url).resp.content
                if len(i.key) != 16:
                    raise Exception(f"key的长度应为16, 实际为{len(i.key)}")
        self.filter()

    def to_2(self):
        if self.res.all_time:
            return
        self.res.url = self.res.url.urljoin(self.res[EXT_VIDEO][-1][-1])
        self.res.set_m3u8_text_by_session()
        self.flush_tasks()

    def filter(self, filter_func=None):
        """_summary_

        Args:
            filter_func (function): args: M3U8VideoList reference
        """
        self.tasks = []
        for i in self.video_url_list:
            if filter_func and filter_func(i):
                continue
            for index, url in enumerate(i.url_list):
                self.tasks.append(
                    M3U8DownloadTask(
                        url,
                        i.key,
                        i.iv,
                        self.res.session,
                        f"{self._f_tspath}{index}.ts",
                    )
                )

    def _do_task(self, task: M3U8DownloadTask, lock: WLock):
        task.get_data(self.mothed)
        lock.acquire()
        self.task_finished_num += 1
        self.progress = round(self.task_finished_num / self.task_all_num, 4)
        if self.task_finished_num == self.task_all_num and not self._merge_ok:
            self._merge_ok = True
            self.status = STATUS_MERGE
            self.merge()
        lock.release()

    def start(self):
        self._merge_ok = False
        self.task_all_num = len(self.tasks)
        self.task_finished_num = 0
        self.status = STATUS_DOWNLOADING
        self.thread.run(self._do_task, self.tasks)

    def merge(self):
        with open(self._file, "ab") as f:
            for file in os.listdir(self._f_tspath):
                file = self._f_tspath + file
                with open(file, "rb") as f1:
                    f.write(f1.read())
        self.status = STATUS_FINISH


# TEST
if __name__ == "__main__":
    res = M3U8Resource(
        "https://v7.fentvoss.com/sdv7/202405/31/rvZPmBdpi513/video/index.m3u8?pay_u="
    )
    res.session.ini.set_proxy(20000)
    res.set_m3u8_text_by_session()
    downloader = res.to_downloader("D:/EasyCode/python/m3u8_test/", "test.mp4")
    downloader.mothed = METHOD_CHECK
    downloader.to_2()
    downloader.start()
    while downloader.status != STATUS_FINISH:
        print(
            downloader.progress,
            downloader.task_finished_num,
            downloader.task_all_num,
            end="\r",
        )
    print(
        "\n",
        downloader.progress,
        downloader.task_finished_num,
        downloader.task_all_num,
        "OK",
        end="",
    )