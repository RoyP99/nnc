'''
Created on Aug 17, 2023

@author: robert
'''
import queue
from flask import Response

class htmlSse(object):
    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=50)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

    def format_sse(self, data: str, event=None) -> str:
        msg = f'data: {data}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
        return msg
    
    def listenUrl(self):
        ''' called when the browser read from SSE '''
    
        def stream():
            messages = self.listen()  # returns a queue.Queue
            while True:
                msg = messages.get()  # blocks until a new message arrives
                yield msg
    
        return Response(stream(), mimetype='text/event-stream')
