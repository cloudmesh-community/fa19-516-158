# Hadoop Clusters With Raspberry Pi

Daivik Uggehalli Dayanand, [fa19-516-158](https://github.com/cloudmesh-community/fa19-516-158)

Akshay Kowshik, [fa19-516-150](https://github.com/cloudmesh-community/fa19-516-150)

Insights: <https://github.com/cloudmesh-community/fa19-516-158/graphs/contributors>

Code Directory:

* <https://github.com/cloudmesh/cm-burn/blob/master/cmburn/>

* <https://github.com/cloudmesh/cloudmesh-inventory/tree/master/cloudmesh/host>

* <https://github.com/cloudmesh-community/fa19-516-158/tree/master/project>

Manual:

* <https://github.com/cloudmesh/cloudmesh_pi_burn/blob/master/cm-pi-burn.md>


.....

:o2: the project is not leveraging the many useful features from cloudmesh, such as 

* inventory, key management, key group management, ssh logins, ..., instead of sometimes listing the technical content, you could have just developed a cms python program and integaated the technical configurations or programs in such a command. We have taught you in the first 2 weeks how to use cms sys command generae to showcase you how you can do this in minutes

:o2: Bash script of maset node needs to be revisisted and you need to
look at cms host which is in inventory. That script should be improved
as needed and made general enough for any cluster deployment on given
hosts. for example if this needs to be added to .bashrc why not develop
a cloudmesh cpmmand

cms host setup bashrc

remember you task is to develop as much as possible cms commands that
makes things easier, which not

cms pi deploy hadoop deploy ....

:o2: This is an unnecessary complex documentation, with lots of details that we realy do not need

I suggest to have a command

```
cms deploy --service=hadoop [--master=NAMEMASTER] [--workers=NAMEWORKERS]
cms deploy --service=hadoop --master=NAMEMASTER --workers=NAMEWORKERS
cms deploy --service=hadoop --master=NAMEMASTER
cms deploy --service=hadoop --workers=NAMEWORKERS
```
## Introduction

Majority of the data in today's world has been stored in HDFS. HDFS
stands for Hadoop Distributed Storage System. The Raspberry Pi provides
to the community a cheap platform with the ability to expose Linux and
other operating systems to the masses. Due to its cost point, it is easy
to buy a PI and experiment with it. As such this platform has been ideal
to lower the entry barrier to advanced computing from the university
level to highschool, middle school and even elementary school. However,
the PI has also been used by universities and even national labs. Due to
its availability and its convenient accessibility, it has become a
staple of our educational pipeline. Due to its price point the PI can
also be used to build cheap clusters putting forward a hardware platform
ideal for experimenting with issues such as networking and cluster
management as an educational tool. Many such efforts exist to use a PI
as a cluster environment.

So it would be a good idea if we could somehow turn such a platform more
powerful by deploying latest technologies such as Hadoop and Spark on
it. Multi cluster Raspberry Pi, where one node can act as the master
node and other nodes act as slaves and the master might be able to
control the slaves.

## Abstract

Deployment of Hadoop on Raspberry Pi Clusters which involves:

* Using CM-BURN command to burn multiple SD cards at once
* Creating a cluster with as many nodes as we have SD cards for

## Architecture

The following 

* A master node maintains knowledge about the distributed file system and schedules resources allocation. It will host two daemons:

1. The NameNode manages the distributed file system and knows where
   stored data blocks inside the cluster are.
2. The ResourceManager manages the YARN jobs and takes care of
   scheduling and executing processes on worker nodes.

* Worker nodes store the actual data and provide processing power to run
  the jobs and will host two daemons:

1. The DataNode manages the physical data stored on the node; it is
   named, NameNode.
2. The NodeManager manages execution of tasks on the node.

## Technologies used

* cm-burn
* Python
* HDFS
* Hadoop

## Implementation

The implememation consists of the following steps

1) Buring the raspian image on the SD card

2) Setting Static IP address on th SD card

3) Setting HostNames on the SD card

4) Implementing SSH so that we can connect from one PI to the other.

5) Downloading Hadoop on the master node 

6) Copying the Hadoop files from the master node across the cluster of nodes using SCP

7) Changing the Configuration Files of Hadoop to set the replication factor,NameNode location,etc

The Major first 3 steps are already implemented using cm-pi-burn. Please go through this [cm-pi-burn](<https://github.com/cloudmesh/cloudmesh_pi_burn/blob/master/cm-pi-burn.md>) for the implementation of the first 3 steps. We will walk through the steps starting from the 4th as to what we have tried on a single node cluster and it works good. We have used bash scipt for our implementation which could be replaced by python script by leveraging the use of host command in the future. The document outlines the steps to be followed to deploy hadoop on a single node cluster.

However we do outline the steps which could be followed to automate the entire process across mutiple nodes(we havent tried this).

After the first 3 steps which is performed using cm-pi-burn each sd card would have a raspbian image on it, static ip address and a host name.Now we have to set up SSH to that we can connect from one Pi in the cluster to the other PI

## Set password, Enable SSH and Reboot Pi

To enable ssh on each Pi, we need to follow these instructions

1. Launch Raspberry Pi Configuration from the Preferences menu
2. Navigate to the Interfaces tab
3. Select Enabled next to SSH
4. Click OK

Alternatively, raspi-config can be used in the terminal:

1. Enter sudo raspi-config in a terminal window
2. Select Interfacing Options
3. Navigate to and select SSH
4. Choose Yes
5. Select Ok
6. Choose Finish

Alternatively we can also use the following commands:

```
sudo systemctl enable ssh
sudo systemctl start ssh
```
## Open SSH

* Installing OpenSSH Server

```
sudo apt-install openssh-server
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.original
sudo chmod a-w /etc/ssh/sshd_config.original
```

* Disable, Enable, Start, Stop SSH Server

```
sudo systemctl disable ssh;
sudo systemctl enable ssh;
sudo systemctl start ssh;
sudo systemctl start ssh;
```

* Adding SSH agent

```
eval $(ssh-agent)
ssh-add
```

## Simplifying SSH

To connect from one Pi to another, having followed only the above
instructions, would require the following series of commands

```
$ ssh pi@192.168.0.10X
pi@192.168.0.10X's password: <enter password – 'raspberry' default>
```

Instead of the above approach we can use SSH aliases which facilitates
easier and faster access

For this we have to edit the `~/.ssh/config` file and add the following
commands

```
Host piX
User pi
Hostname 192.168.0.10X
```

X needs to be replaced with the respective PI number

The output screen is depicted as follows:

```
$ ssh piX
pi@192.168.0.10X's password: <enter password>
```

This can be further simplified using the public/private key pairs

:o: this is too complex we just use `id_ras.pub`

```
ssh-keygen –t ed25519
```

This will generate a public and private key pair within the directory
`~/.ssh/` which can be used to securely ssh without entering a password.
One of these files will be called id_ed25519, this is the private key.
The other, id_ed25519.pub is the public key. The public key is used to
communicate with the other Pis, and the private key never leaves its
host machine and should never be moved or copied to any other device.

To overcome this problem each public key needs to be concatenated to the
`~/.ssh/authorized_keys` file on every other pi.

On all other Pis run the following command:

```bash
$ cat ~/.ssh/id_ed25519.pub | ssh pi@192.168.0.101 'cat >> .ssh/authorized_keys'
```

This concatenates Pi #2's public key file to Pi #1's list of authorized
keys, giving Pi #2 permission to ssh into Pi #1 without a password. We
should also do this for Pi #1, so that when we copy the completed
authorized_keys file to the other Pis, they all have permission to ssh
into Pi #1, as well(assuming that Pi1 acts as the  master node).

```bash
$ cat .ssh/id_ed25519.pub >> .ssh/authorized_keys
```

Once this is done, as well as the previous section, ssh-ing is as easy
as:

```bash
$ssh pi1
```

To replicate the passwordless ssh across all Pis, simply copy the two
files mentioned above from Pi #1 to each other Pi using scp

```bash
$ scp ~/.ssh/authorized_keys piX:~/.ssh/authorized_keys
$ scp ~/.ssh/config piX:~/.ssh/config
```

## Single Node(Master) set up Hadoop

:o2: please replace this with the host command in inventory

we need

scp using parameterized notation
ssh using parameterized notation
register workers and master in inventory
restart using parameterized notation
shutdown using parameterized notation
rsync using parameterized notation

figure out what realy needs to be added to the .bashrc. we can install
cloudmeh an oall machines fir the ssh commands for example

### Bash Script of Master Node

#### To copy the files in /opt/hadoop to all Pis

:o2: this can be done as a script and hidden

for pi in $(otherpis); do rsync -avxP $HADOOP_HOME $pi:/opt; done

This may be needed to be added to .bashrc

```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-armhf
export HADOOP_HOME=/opt/hadoop
export SPARK_HOME=/opt/spark
export PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$PATH
export HADOOP_HOME_WARN_SUPRESS=1
```

#### Set JAVA_HOME

:o2: this can be done as a script and hidden

* To find Java path

```bash
update-alternatives --display java
```

* Remove /bin/java - On Debian, the link is

  :o: command is not given

  /usr/lib/jvm/java-11-openjdk-armhf/bin/java, so JAVA_HOME should be
  /usr/lib/jvm/java-11-openjdk-armhf.

* Update the hadoop-env.sh under ~/hadoop/etc/hadoop as:

  :o: this can be done with a script and hidden

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-armhf

#### Hadoop installation

:o2: this can be done as script and hidden

```bash
wget "https://archive.apache.org/dist/hadoop/common/hadoop-3.2.0/hadoop-3.2.0.tar.gz"
tar -xzf hadoop-3.2.0.tar.gz
sudo mv ~/hadoop-3.2.0 /opt/hadoop
```

We can use clustercp function to copy the same file across all the
cluster so that hadoop is installed across all the nodes

After the above step change the permissions on the directory using:

```bash
$ sudo chown pi:pi -R /opt/hadoop
```

You can also verify if hadoop has been installed correctly by checking
the version

```
$ cd && hadoop version | grep Hadoop
```

The output will be

```
Hadoop 3.2.0
```

#### Spark installation

```bash
$ wget "https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz"
$ tar -xzf spark-2.4.3-bin-hadoop2.7.tgz
$ sudo mv ~/spark-2.4.3-bin-hadoop2.7 /opt/spark
```

We can use clustercp function to copy the same file across all the
cluster so that hadoop is installed across all the nodes

After the above step change the permissions on the directory using:

```bash
$ sudo chown pi:pi -R /opt/spark
```

You can also verify if hadoop has been installed correctly by checking
the version

```bash
$ cd && spark version | grep spark

```

The output will be as follows

```
... version 2.4.3 ... Using Scala version 2.11.12 ...
```

#### Versions of Hadoop and Spark

```bash
$ cd && hadoop version | grep Hadoop
$ cd && spark-shell --version
```

#### HDFS

To get the Hadoop Distributed File System (HDFS) up and running, modify
the following configuration files which are under
/opt/hadoop/etc/hadoop.

1. Update core-site.xml file to set the NameNode location to Master on
   port 9000:

```
<configuration>
  <property>
    <name>fs.default.name</name>
    <value>hdfs://pi1:9000</value>
  </property>
</configuration>
```

2. To set path for HFDS, edit hdfs-site.xml. dfs.replication, indicates
   how many times data is replicated in the cluster. Set 4 to have all the
   data duplicated four nodes. Don’t enter a value higher than the actual
   number of worker nodes.

```
<configuration>
        <property>
                <name>dfs.datanode.data.dir</name>
                <value>file:///opt/hadoop_tmp/hdfs/datanode</value>
        </property>
        <property>
                <name>dfs.namenode.name.dir</name>
                <value>file:///opt/hadoop_tmp/hdfs/namenode</value>
        </property>
        <property>
                <name>dfs.replication</name>
                <value>4</value>
        </property>
</configuration>
```

3. To set Yarn as Job Scheduler, edit mapred-site.xml, setting YARN as
   the default framework for MapReduce operations.

```
<configuration>
        <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
        </property>
        <property>
                <name>yarn.app.mapreduce.am.resource.mb</name>
                <value>256</value>
        </property>
        <property>
                <name>mapreduce.map.memory.mb</name>
                <value>128</value>
        </property>
        <property>
                <name>mapreduce.reduce.memory.mb</name>
                <value>128</value>
        </property>
</configuration>
```

4. Edit yarn-site.xml, which contains the configuration options for
   YARN.

```
<configuration>
  <property>
    <name>yarn.acl.enable</name>
    <value>0</value>
  </property>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>pi1</value>
  </property>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>
  <property>
    <name>yarn.nodemanager.resource.memory-mb</name>
    <value>900</value>
  </property>
  <property>
    <name>yarn.scheduler.maximum-allocation-mb</name>
    <value>900</value>
  </property>
  <property>
    <name>yarn.scheduler.minimum-allocation-mb</name>
    <value>64</value>
  </property>
  <property>
    <name>yarn.nodemanager.vmem-check-enabled</name>
    <value>false</value>
  </property>
</configuration>
```

#### Format HDFS

```bash
$ hdfs namenode -format -force
```

#### Boot HDFS

* Start HDFS by running the following script from master node:

```bash
$ start dfs.sh
```

* Start YARN with the following script from master node:

```bash
$ start yarn.sh
```

#### Test HDFS

Check HDFS is working by creating a temporary directory

```bash
$ hadoop fs -mkdir /tmp
$ hadoop fs -ls /
$ jps
```

#### Test Hadoop and Spark working together

```bash
$ hadoop fs -put $SPARK_HOME/README.md /
```

## References

* <https://raspberrytips.com/install-raspbian-raspberry-pi/>
* <https://raspberrytips.com/raspberry-pi-cluster/>
* <https://www.raspberrypi.org/documentation/remote-access/ip-address.md>
* <https://dqydj.com/raspberry-pi-hadoop-cluster-apache-spark-yarn/>
* <https://www.mocomakers.com/building-a-raspberry-pi-cluster-with-apache-spark/>
* <https://tekmarathon.com/2017/02/16/hadoop-and-spark-installation-on-raspberry-pi-3-cluster-part-4/amp/>
* <https://medium.com/@glmdev/building-a-raspberry-pi-cluster-784f0df9afbd>
* <https://dev.to/awwsmm/building-a-raspberry-pi-hadoop-spark-cluster-8b2>
* <https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/>
* <https://www.linode.com/docs/databases/hadoop/install-configure-run-spark-on-top-of-hadoop-yarn-cluster/>
