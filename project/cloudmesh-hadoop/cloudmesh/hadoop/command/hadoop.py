from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.hadoop.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.parameter import Parameter

class HadoopCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_hadoop(self, args, arguments):
        """
        ::

          Usage:
                hadoop shutdown HOSTS
                hadoop uname HOSTS
                hadoop deploy HOSTS [--master HOST]

                hadoop list

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

          Description:

             The command

                hadoop deploy HOSTS [--master HOST]

              deploeys a hadoop cluster on the given nodes,
              where the first node its the master. The master
              node can be overwriteen

        """

        VERBOSE(arguments)

        m = Manager()

        if arguments.shutdown:

            hosts = Parameter.expand(arguments["HOSTS"])
            print (hosts)
            m.shutdown(hosts)

        elif arguments.uname:

            hosts = Parameter.expand(arguments["HOSTS"])
            print (hosts)
            m.uname(hosts)

        elif arguments.deploy:

            hosts = Parameter.expand(arguments["HOSTS"])

            if ["--master"] in arguments:
                master = arguments["--master"]
                workers = hosts
                #
                # remove the master from the list.
                #
                workers = list(set(hosts) - master)

            else:
                master = hosts[0]
                workers = hosts[1:]

            print (hosts)
            print (master)
            print(workers)

            # do teh deployment for master and for workers

            for host in workers:
                print ("worker", host)
                # ????
            for host in master:
                print("master", host)
                # ????

        return ""
