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

    def activate(self):
        """Plugin activation function"""
        super().activate()
        if self.config['POINTS_TIMER_S'] > 0:
            self.start_poller(self.config['POINTS_TIMER_S'], self.add_timer_points)

        #UserPoints maps user name to point value
        if not 'UserPoints' in self:
            self['UserPoints'] = {}

    def add_timer_points(self):
        """Add points to every user present when this function is called"""
        room = self._bot.query_room()
        for user in room.occupants():
            # print(user.person())
            # print(user.nick())
            #TODO: Check status
            self['UserPoints'][user.person()] += self.config['POINTS_PER_TICK']

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
