#!python

from errbot import BotPlugin, botcmd

from collections import defaultdict
from itertools import chain

CONFIG_TEMPLATE = {
    'ROOM': 'changeme',
    'POINTS_TIMER_S': 60,
    'POINTS_PER_TICK': 5,
    'POINT_NAME': 'point'
}

class PointsPlugin(BotPlugin):
    """Plugin for tracking user points"""

    def activate(self):
        """Plugin activation function"""
        super().activate()
        if self.config['POINTS_TIMER_S'] > 0:
            self.start_poller(self.config['POINTS_TIMER_S'], self.add_timer_points)

        #UserInfo maps user name to point value
        if not 'UserInfo' in self:
            self['UserInfo'] = defaultdict(dict)

    @botcmd
    def points(self, mess, args):
        """Respond to user with the number of points they have accumulated."""

        #TODO: Make this smarter for general words
        point_plural = '{0}s'.format(self['POINT_NAME'])
        if mess.frm.person() is not in self['UserInfo']:
            return '{0}: No {1} recorded yet'.format(mess.frm.nick(), point_plural)

        return '[{0}]: {1} {2} '.format(mess.frm.nick(), pts, point_plural)
        pts = self['UserInfo'][mess.frm.person()]['pts']

    @arg_botcmd('user', admin_only=True)
    @arg_botcmd('value', admin_only=True)
    def points_set(self, mess, user, value):
        """Set a users points to a particular value"""
        self['UserInfo'][user]['pts'] = int(value)

    @arg_botcmd('user', admin_only=True)
    @arg_botcmd('value', admin_only=True)
    def points_add(self, mess, user, value):
        """Add points to a particular user"""
        self['UserInfo'][user]['pts'] += int(value)

    @arg_botcmd('user', admin_only=True)
    @arg_botcmd('value', admin_only=True)
    def points_remove(self, mess, user, value):
        """Add points to a particular user"""
        self['UserInfo'][user]['pts'] -= int(value)

    def add_timer_points(self):
        """Add points to every user present when this function is called"""
        room = self._bot.query_room()
        for user in room.occupants():
            self['UserInfo'][user.person()]['pts'] += self.config['POINTS_PER_TICK']

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
