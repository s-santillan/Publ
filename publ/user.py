""" Authenticated user functionality """

import collections
import configparser

import flask
from werkzeug.utils import cached_property

from . import caching, config


@caching.cache.memoize()
def get_groups():
    """ Get the user->groups mappings """

    # We only want empty keys; \000 is unlikely to turn up in a well-formed text file
    cfg = configparser.ConfigParser(delimiters=('\000'), allow_no_value=True)
    cfg.read(config.user_list)

    groups = collections.defaultdict(set)

    # populate the group list for each member
    for group, members in cfg.items():
        for member in members.keys():
            groups[member].add(group)

    return groups


class User(caching.Memoizable):
    """ An authenticated user """

    def __init__(self, me):
        self._me = me

    def _key(self):
        return User, self._me

    @cached_property
    def name(self):
        """ The federated identity name of the user """
        return self._me

    @property
    @caching.cache.memoize()
    def groups(self):
        """ The group memberships of the user """
        groups = get_groups()
        result = set()
        pending = collections.deque()

        if self._me:
            pending.append(self._me)

        while pending:
            check = pending.popleft()
            if check not in result:
                result.add(check)
                pending += groups.get(check, [])

        return result

    @property
    def is_admin(self):
        """ Returns whether this user has administrator permissions """
        return config.admin_group and config.admin_group in self.groups


def get_active():
    """ Get the active user and add it to the request stash """
    if flask.session.get('me'):
        return User(flask.session['me'])

    return None
