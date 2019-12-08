import os
from cloudmesh.common.util import writefile

class Manager(object):

    def __init__(self):
        print("init {name}".format(name=self.__class__.__name__))

    def list(self, parameter):
        print("list", parameter)

    def get_hosts(self):
         #.... grep "pi" /etc/hosts | awk '{print $2}' | grep -v $(hostname)
        raise NotImplementedError
        
    def get_hadoop(self):
        
        #downloads the hadoop on a given node and copy the same file across the cluster of commands using the scp command

    def run(self, hosts=None, command=None, sudo=""):
        user = "pi"
        for host in hosts:
            print(f"ssh {user}@{host} {sudo} {command}")
            #os.system(f"ssh {user}@{host} {sudo} {command}")

    def cp(self, hosts, source, target):
        user = "pi"
        for host in hosts:
                os.system(f"scp {source} {target}")

        # cat $1 | ssh $pi "sudo tee $1" > /dev/null 2>&1

    def restart(self, hosts):
        #self.run(hosts=hosts, "shutdown -r now", sudo="sudo")
        pass

    def shutdown(self, hosts):
        print("shutdown", hosts)
        self.run(hosts=hosts, command="shutdown now", sudo="sudo")

    def uname(self, hosts):
        print("uname", hosts)
        self.run(hosts=hosts, command="uname -a")

    def rsync(self, hosts, source, destination):
        #
        # easy excersie for students
        #
        # To copy the files in /opt/hadoop to all Pis
        #function copyconfig {
        #        for pi in $(otherpis); do rsync -avxP $HADOOP_HOME $pi:/opt; done
        #}
        pass

    def setup_bashrc(self, hosts):
        exports = """
        export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-armhf
        export HADOOP_HOME=/opt/hadoop
        export SPARK_HOME=/opt/spark
        export PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$PATH
        export HADOOP_HOME_WARN_SUPRESS=1
        """
        writefile("tmp", exports)
        self.cp(hosts, "tmp", "tmp")
        self.run(hosts, "cat tmp >> .bashrc")
