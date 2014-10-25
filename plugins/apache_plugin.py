##
# Example barbican plugin
##

from plugins import plugin_classes
import time
import re


class ApachePlugin(plugin_classes.MonitoringPlugin):
    module_name = "apache"

    def handle(self, line):

        try:
            print re.findall(self.log_regex, line.strip()).groups()
        except:
            print line.strip()
            return

    def run(self):
        print "Activated apache"
        f = open('/var/log/apache2/access_log', 'r')
        while True:  # Continuously watch for changes
            line = ''
            while len(line) == 0 or line[-1] != '\n':  # Read in new lines
                tail = f.readline()
                if tail == '':
                    time.sleep(0.1)
                    continue
                line += tail
            self.handle(line)
