##
# Example barbican plugin
##

from plugins import plugin_classes


class ExamplePlugin(plugin_classes.MonitoringPlugin):
    module_name = "example"

    def run(self):
        print "Activated example plugin"
        return
