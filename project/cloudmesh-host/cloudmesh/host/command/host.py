from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.host.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE

class HostCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_host(self, args, arguments):
        """
        ::

          Usage:
              host scp NAMES SOURCE DESTINATION
              host ssh NAMES COMMAND
              host keys get NAMES
              host keys put NAMES

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """

        VERBOSE(arguments)


        if arguments.scp:

            raise NotImplementedError

        elif arguments.ssh:
            raise NotImplementedError

        elif arguments.keys and arguments.get:
            raise NotImplementedError

        elif arguments.keys and arguments.put:
            raise NotImplementedError


        return ""
