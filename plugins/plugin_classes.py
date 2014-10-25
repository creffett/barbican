##
# Example barbican plugin
##

from yapsy.IPlugin import IPlugin


class MonitoringPlugin(IPlugin):
    hostname = "default"
    module_name = "none"

    def set_hostname(self, hostname):
        self.hostname = hostname

    def set_config_file(self, config_file):
        self.config_file = config_file


class FirewallPlugin(IPlugin):
    def set_config_file(self, config_file):
        self.config_file = config_file
