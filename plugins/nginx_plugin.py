##
# Example barbican plugin
##

from plugins import plugin_classes
import time


class NginxPlugin(plugin_classes.MonitoringPlugin):
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
