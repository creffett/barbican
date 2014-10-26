##
# Example barbican plugin
##

from plugins import plugin_classes
import SocketServer
import json
import iptc
import threading


class IptablesPlugin(plugin_classes.FirewallPlugin):
    hostname = "default"
    module_name = "iptables"

    class JSONHandler(SocketServer.BaseRequestHandler):
        def timer_delete(self, host, port):
            table = iptc.Table(iptc.Table.FILTER)
            table.autocommit = False
            chain = iptc.Chain(table, "INPUT")
            for rule in chain.rules:
                port_matches = False
                for match in rule.matches:
                    if match.name == "tcp" and match.dport == port:
                        port_matches = True
                if rule.src == "%s/255.255.255.255" % host and port_matches:
                    print "deleted ", rule
                    chain.delete_rule(rule)
            table.commit()
            table.autocommit = True

        def handle(self):
            try:
                chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
                action_message = json.loads(self.request.recv(1024).strip())
		if socket.gethostbyname(action_message["data"]["host"]) == action_message["data"]["host"]:
			host = action_message["data"]["host"]
		else:
			host = socket.gethostbyname(action_message["data"]["host"])
                port = action_message["data"]["port"]
                time = action_message["data"]["time"]
                print "Blocking host %s on port %s for duration %s" % \
                    (host, port, time)
                rule = iptc.Rule()
                rule.src = host
                rule.protocol = "tcp"
                match = rule.create_match("tcp")
                match.dport = port
                rule.create_target("DROP")
                chain.insert_rule(rule)
                if (time == 0):
                    return
                else:
                    thread = threading.Timer(float(time), self.timer_delete, [host, port])
                    thread.start()

            except Exception, e:
                print "Exception in iptables plugin receiving JSON data: ", e

    def run(self):
        print "Activating iptables listener"
        listener = SocketServer.ThreadingTCPServer(('0.0.0.0', 1337),
                                                   self.JSONHandler)
        listener.serve_forever()

        return

    def set_hostname(self, hostname):
        self.hostname = hostname

    def set_config_file(self, config_file):
        self.config_file = config_file
