#-*- coding: UTF-8 -*-

class Queue:
    def __init__(self,max_size):
        self.max_size = int(max_size)
        self.queue = []

    def put(self,data):
        if self.max_size > 0:
            if self.full():
                raise ValueError('Queue is full!')
            else:
                self._put(data)

    def get(self):
        if self._queue_size() > 0:
            result = self._get()
            empty_flag = False
        else:
            result = None
            empty_flag = True
        return result

    def empty(self):
        if self._queue_size() == 0:
            return True
        else:
            return False

    def full(self):
        if self._queue_size() == self.max_size:
            return True
        else:
            return False

    def _put(self,data):
        self.queue.append(data)

    def _get(self):
        result = self.queue[0]
        self.queue.pop(0)
        return result

    def _queue_size(self):
        return len(self.queue)