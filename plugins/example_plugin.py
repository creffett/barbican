##
# Example barbican plugin
##

from yapsy.IPlugin import IPlugin


class ExamplePlugin(IPlugin):
    def print_name(self):
            print "This is the example plugin"

    def run(self):
        print "Activated example plugin"
        return

    def generate_json():
        return
