from cloudmesh.common3.Shell import Shell
from pprint import pprint

class Host (object):

    @staticmethod
    def ssh(names, command, output="lines"):
        """

        :param names:
        :param command:
        :param output:
        :return:
        """

        results = []
        for name in names:
            print(f"ssh {name} {command}")

            result = Shell.run(command)

            if output == "lines":
                lines = result.split("\n")
                results.append((name, lines))
            elif output == "string":
                results.append((name, result))

        return results

    @staticmethod
    def scp(source, destinations, output="lines"):
        """

        :param names:
        :param command:
        :param output:
        :return:
        """

        results = []
        for destination in destinations:
            command = (f"scp  {source} {destination}")

            print (command)

            result = Shell.run(command)

            if output == "lines":
                lines = result.split("\n")
                results.append((destination, lines))
            elif output == "string":
                results.append((destination, result))

        return results

    @staticmethod
    def concatenate_keys(results):
        result = ""
        for entry in results:
            name, key = entry
            key = ' '.join(key)
            result = result + str(key) + "\n"
        result = result.strip()
        return result
