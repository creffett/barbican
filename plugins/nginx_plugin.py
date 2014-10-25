##
# Example barbican plugin
##

from yapsy.IPlugin import IPlugin
import time
import re
import os

class NginxPlugin(IPlugin):
    hostname = "default"
    module_name = "nginx"
    def handle(self, line):
        print line.strip()

    def run(self):
        print "Activated nginx"
        f = open('/var/log/nginx/access_log', 'r')
        while True:  # Continuously watch for changes
            line = ''
            while len(line) == 0 or line[-1] != '\n':  # Read in new lines
                tail = f.readline()
                if tail == '':
                    time.sleep(0.1)
                    continue
                line += tail
            self.handle(line)

    def set_hostname(self, hostname):
        self.hostname = hostname

    def set_config_file(self, config_file):
        self.config_file = config_file
