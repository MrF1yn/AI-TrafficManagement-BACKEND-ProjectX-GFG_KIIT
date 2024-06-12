import ctypes
import json
import time
from channels.generic.websocket import WebsocketConsumer
from django.core.files.storage import FileSystemStorage
import threading

from . import ml_model

threads = {}


class multithreaded_model(threading.Thread):
    def __init__(self, video_dir, socket):
        threading.Thread.__init__(self)
        self.video_dir = video_dir
        self.socket = socket

    def run(self):

        # target function of the thread class
        try:
            ml_model.predict(self.video_dir, self.socket)
        finally:
            print('ended')

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(self.scope["user"].username)
        # self.close()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        if text_data == "start":
            fs = FileSystemStorage()
            [folders, files] = fs.listdir("uploaded_videos/" + self.scope["user"].username + "/")
            # video_dir = ["uploaded_videos/"+self.scope["user"].username+"/"+files]
            video_dir = ["uploaded_videos/" + self.scope["user"].username + "/" + file for file in files]
            self.send(text_data=json.dumps(video_dir))
            t1 = multithreaded_model(video_dir, self)
            threads[self.scope["user"].username] = t1
            t1.start()
            return
        if text_data == "stop":
            if threads[self.scope["user"].username]:
                thread = threads[self.scope["user"].username]
                thread.raise_exception()
                thread.join()
