##
# Example barbican plugin
##

from yapsy.IPlugin import IPlugin


class ExamplePlugin(IPlugin):
    hostname = "default"
    module_name = "example"

    def run(self):
        print "Activated example plugin"
        return

    def set_hostname(self, hostname):
        self.hostname = hostname

    def set_config_file(self, config_file):
        self.config_file = config_file
