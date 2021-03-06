from django.conf import settings
from django.contrib.auth.models import Permission

from admincommand.models import AdminCommand
from sneak.query import ListQuerySet


class CommandQuerySet(ListQuerySet):
    """
    Custom QuerySet to list runnable commands
    """

    def __init__(self, user, value=None):
        self.user = user
        if value is None:
            self.value = self.filter().value
        else:
            self.value = value

    def _clone(self):
        return type(self)(self.user, self.value)

    def filter(self, *args, **kwargs):
        all_commands = []
        for command in AdminCommand.all():
            # only list commands that the user can run
            # to avoid useless 503 messages
            full_permission_codename = "admincommand.%s" % command.permission_codename()
            if self.user.has_perm(full_permission_codename):
                all_commands.append(command)
        return type(self)(self.user, all_commands)
