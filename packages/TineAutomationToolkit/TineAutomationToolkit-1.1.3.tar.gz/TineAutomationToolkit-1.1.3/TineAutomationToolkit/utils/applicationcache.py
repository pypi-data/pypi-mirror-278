# -*- coding: utf-8 -*-

from robot.utils import ConnectionCache

class ApplicationCache(ConnectionCache):

    def __init__(self):
        ConnectionCache.__init__(self, no_current_msg='No current application')
        self._closed = set()

    def close(self):
        if self.current:
            application = self.current
            application.quit()
            self.current = self._no_current
            self.current_index = None
            self._closed.add(application)