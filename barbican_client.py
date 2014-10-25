#!/usr/bin/python
##
# Main python module of the barbican client
##

from yapsy.PluginManager import PluginManager
from ConfigParser import ConfigParser
from argparse import ArgumentParser
from threading import Thread
from plugins.plugin_classes import MonitoringPlugin, FirewallPlugin
import logging
import os

plugin_manager = PluginManager()


def initializeBarbican(config_path):
    '''Read in config files and activate plugins'''
    config = ConfigParser()
    config.readfp(open(config_path))

    plugin_path = os.path.join(os.getcwd(), config.get("barbican_client",
                                                       "plugin_dir"))
    plugin_manager.setPluginInfoExtension("barbican-plugin")
    plugin_manager.setPluginPlaces([plugin_path])
    # Set up categories
    plugin_manager.setCategoriesFilter({
        "Monitoring": MonitoringPlugin,
        "Firewall": FirewallPlugin
        })
 
    plugin_manager.collectPlugins()

    for plugin_info in plugin_manager.getAllPlugins():
        print plugin_info, plugin_info.name

    print "Activating monitoring plugins"
    for plugin_info in plugin_manager.getPluginsOfCategory("Monitoring"):
        plugin_manager.activatePluginByName(plugin_info.name)

    for plugin_info in plugin_manager.getPluginsOfCategory("Monitoring"):
        plugin_info.plugin_object.set_hostname(config.get("barbican_client", "hostname"))
        plugin_info.plugin_object.set_config_file(config_path)

    print "Activating firewall"
    firewall_plugin = config.get("firewall_plugin")
    if firewall_plugin is not None:
        plugin_manager.activatePluginByName(firewall_plugin)
    else:
        plugin_manager.activatePluginByName("iptables plugin")

    return


def runBarbican():
    threads = []
    for plugin_info in plugin_manager.getAllPlugins():
        threads.append(Thread(target=plugin_info.plugin_object.run))

    for t in threads:
        t.daemon = True  # Supposedly lets me Ctrl-C with threads running
        t.start()

    for t in threads:
        t.join()


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = ArgumentParser(description="Activate barbican")
    parser.add_argument("--config", dest="config_path",
                        help="Path to the configuration file",
                        default="config/barbican_client.conf")
    args = parser.parse_args()
    initializeBarbican(args.config_path)
    runBarbican()

if __name__ == '__main__':
    main()
