import threading
import time

WLock = threading.Lock
class WMultiThread:

    def __init__(self, thread_num: int = 8):
        # 线程数量
        self.thread_num = thread_num
        # 当前运行函数
        self._func = None
        # 当前线程锁
        self._lock = threading.Lock()
        # 可迭代任务
        self._tasks = None
        self._begin_time: int = 0
        self._end_time: int = 0
        self._is_running = False

    def _run_func(self, *args):
        try:
            while not self._func(next(self._tasks), self._lock, *args):
                pass
        except StopIteration:
            pass
        self._lock.acquire()
        self._end_time = time.time()
        self._is_running = False
        
        self._lock.release()

    def run(self, func, _tasks, *args):
        """

        :param _tasks: 所需完成的任务, 可迭代对象
        :param func: 函数的第一个参数必须是task, 第二个必须是锁WLock
        :return: NAN
        """
        self._func = func
        self._is_running = True
        self._begin_time = time.time()
        self._tasks = iter(_tasks)
        for i in range(self.thread_num):
            threading.Thread(target=self._run_func, args=args).start()

    @property
    def begin_time(self):
        return self._begin_time

    @property
    def end_time(self):
        return self._end_time

    def is_running(self):
        return self._is_running
    
    
if __name__ == "__main__":
    ts = range(100)

    cnt = 0
    def test(i, l):
        global cnt
        cnt += 1
        time.sleep(0.01)


    th = WMultiThread(32)
    th.run(test, ts)
    while th.is_running():
        time.sleep(1)
    t1 = time.time()
    for i in range(100):
        test
    print(time.time() - t1)
    print(th.end_time - th.begin_time)
    print(cnt)
