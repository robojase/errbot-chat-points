#!python

from errbot import BotPlugin, botcmd

from itertools import chain

CONFIG_TEMPLATE = {
    'ROOM': 'changeme',
    'POINTS_TIMER_S': 60,
    'POINTS_PER_TICK': 5
}

class PointsPlugin(BotPlugin):
    """Plugin for tracking user points"""

    def return_configuration_template(self):
        """Returns default configuration template"""
        return CONFIG_TEMPLATE

    def configure(self, configuration):
        """Function to process configuration setting"""
        if configuration is not None and configuration != {}:
            config = dict(chain(CONFIG_TEMPLATE.items(),
                                configuration.items()))
        else:
            config = CONFIG_TEMPLATE
        super(PluginExample, self).configure(config)
