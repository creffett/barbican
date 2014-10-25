#!/usr/bin/python
##
# Main python module of the barbican client
##

from yapsy.PluginManager import PluginManager
from ConfigParser import ConfigParser
from argparse import ArgumentParser
from threading import Thread
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
    plugin_manager.collectPlugins()

    print "Activating plugins"
    for plugin_info in plugin_manager.getAllPlugins():
        plugin_manager.activatePluginByName(plugin_info.name)
    return


def runBarbican():
    threads = []
    for pluginInfo in plugin_manager.getAllPlugins():
        threads.append(Thread(target=pluginInfo.plugin_object.run))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def main():
    logging.basicConfig()

    parser = ArgumentParser(description="Activate barbican")
    parser.add_argument("--config", dest="config_path",
                        help="Path to the configuration file",
                        default="config/barbican_client.conf")
    args = parser.parse_args()
    initializeBarbican(args.config_path)
    runBarbican()

if __name__ == '__main__':
    main()
