import time

from PyQt5.QtCore import QThread, pyqtSignal


class MyThread(QThread):
    signal = pyqtSignal(tuple)

    def __init__(self, fun, param=None):
        self.fun = fun
        self.param = param
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        start_ = time.time()
        result = self.fun(self.param)

        span = 0.5 - (time.time() - start_)
        if span > 0:
            time.sleep(span)
        self.signal.emit(result)
