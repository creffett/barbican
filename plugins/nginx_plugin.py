##
# Example barbican plugin
##

from yapsy.IPlugin import IPlugin
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class LogChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print "Got it!", event


class ApachePlugin(IPlugin):

    def run(self):
        print "Activated nginx"

        event_handler = LogChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, path='/tmp/test/', recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def print_name(self):
        print "This is the Apache log monitor plugin"

    def generate_json(self):
        return
