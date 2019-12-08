# Hadoop Clusters With Raspberry Pi

Akshay Kowshik, [fa19-516-150](https://github.com/cloudmesh-community/fa19-516-150)

Daivik Uggehalli Dayanand, [fa19-516-158](https://github.com/cloudmesh-community/fa19-516-158)

Insights: https://github.com/cloudmesh-community/fa19-516-158/graphs/contributors

Code Directory:

https://github.com/cloudmesh/cm-burn/blob/master/cmburn/pi/cmpiburn.py

https://github.com/cloudmesh/cloudmesh-inventory/tree/master/cloudmesh/host

https://github.com/cloudmesh-community/fa19-516-158/tree/master/project

:o2: you miss the basic information, see other project, there are a bunch of links to be added, you do not even include your names and hids ..... 

:o2: Bash script of maset node needs to be revisisted and you need to
look at cms host which is in inventory. That script should be improved
as needed and made general enough for any cluster deployment on given
hosts. for example if this needs to be added to .bashrc why not develop a cloudmesh cpmmand 

cms host setup bashrc 

remember you task is to develop as much as possible cms commands that makes things easier, which not

cms pi deploy hadoop deploy ....

## Introduction

Majority of the data in today's world has been stored in HDFS. HDFS stands for Hadoop Distributed Storage System. The Raspberry Pi provides to the community a cheap platform with the ability to expose Linux and other operating systems to the masses. Due to its cost point, it is easy to buy a PI and experiment with it. As such this platform has been ideal to lower the entry barrier to advanced computing from the university level to highschool, middle school and even elementary school. However, the PI has also been used by universities and even national labs. Due to its availability and its convenient accessibility, it has become a staple of our educational pipeline. Due to its price point the PI can also be used to build cheap clusters putting forward a hardware platform ideal for experimenting with issues such as networking and cluster management as an educational tool. Many such efforts exist to use a PI as a cluster environment.

So it would be a good idea if we could somehow turn such a platform more powerful by deploying latest technologies such as Hadoop and Spark on it. Multi cluster Raspberry Pi, where one node can act as the master node and other nodes act as slaves and the master might be able to control the slaves.

## Abstract

Deployment of Hadoop and Spark on Raspberry Pi Clusters which involves:
* Using CM-BURN command to burn multiple SD cards at once
* Deploying Hadoop and Spark on Raspberry PI Clusters
* Creating a cluster with as many nodes as we have SD cards for

## Architecture

* A master node maintains knowledge about the distributed file system and schedules resources allocation. It will host two daemons:

1. The NameNode manages the distributed file system and knows where stored data blocks inside the cluster are.
2. The ResourceManager manages the YARN jobs and takes care of scheduling and executing processes on worker nodes.

* Worker nodes store the actual data and provide processing power to run the jobs and will host two daemons:

1. The DataNode manages the physical data stored on the node; it’s named, NameNode.
2. The NodeManager manages execution of tasks on the node.

## Technologies used

* cm-burn
* Python
* HDFS
* Hadoop
* Spark

## Implementation

* Multiple Hosts using cloudmesh parameter: cms sys command generate hadoop
<https://github.com/cloudmesh-community/fa19-516-158/blob/master/project/cloudmesh-hadoop/cloudmesh/hadoop/api/manager.py>

The operating system used for the Raspberry Pi is Raspbian, a Debian-based operating system developed and maintained by the Raspberry Pi Foundation. It is the Foundation's official supported OS.

* To install Raspbian, download the image from the official Raspberry Pi website. Different versions of images can be found with <https://downloads.raspberrypi.org/raspbian_lite/images/>

* Download latest Raspbian Buster Lite image from <https://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2019-09-30/>

* This .img file needs to be burned on the SD card manually. To do this, use Etcher on Windows to select the .img file to burn the image onto the SD card. This is time consuming and has to be repeated for every SD card. Instead, we can write a program to automate this process.

* Clone the cm-burn repository <https://github.com/cloudmesh/cm-burn.git> to the local system. Insert a blank SD card and use the cm-pi-burn.py script to burn the Raspbian image onto the blank SD card.

* In a root shell:

```
# cm-pi-burn.py image get latest
# cm-pi-burn.py image ls
# cm-pi-burn.py create --image=2019-09-26-raspbian-buster-lite
                       --device=/dev/mmcblk0
                       --hostname=red[2-6] --ipaddr=192.168.1.[2-6]
                       --sshkey=id_ed25519
```
This gets the latest image and burns images sequentially on the SD card.

## Setting static IP for each Pi on Network Switch

To facilitate easy networking of the Pis, we are  going to set static IP addresses for each Pi on the network switch. we will number the Pis 1-8 (inclusive) according to their positions on the network switch and in the carrying case.
To enable user-defined, static IP addresses, edit the file /etc/dhcpcd.conf on each Pi and uncomment/edit the lines:

```
interface eth0
static ip_address=192.168.0.10X/24
```
where, X denotes the number to be assigned for every Pi. After this change has been made on a particular Pi, reboot the machine. Once this is done for all Pis in the network, they should all be able to ping each other at those addresses.

## Set password, Enable SSH and Reboot Pi

To enable ssh on each Pi, we need to follow these instructions

1) Launch Raspberry Pi Configuration from the Preferences menu
2) Navigate to the Interfaces tab
3) Select Enabled next to SSH
4) Click OK

Alternatively, raspi-config can be used in the terminal:

1) Enter sudo raspi-config in a terminal window
2) Select Interfacing Options
3) Navigate to and select SSH
4) Choose Yes
5) Select Ok
6) Choose Finish

Alternatively we can also use the following commands:
```
sudo systemctl enable ssh
sudo systemctl start ssh
```
## Hostname

Initially, all the Pis are known as raspberrypi, and have a single user, pi: Two files must be edited: /etc/hosts and /etc/hostname.  In the /etc/hostname we change the hostnames to pi1,pi2,pi3 and so on

```
$ hostname
raspberrypi

$whoami
pi
```


This is very confusing if we're constantly moving back and forth between the different Pis on the network. To simplify this, assign each Pi a hostname based on its position in the network switch. Pi #1 will be known as pi1, Pi #2 as pi2, and so on.
In order to accomplish this, we need to edit 2 files /etc/hosts and /etc/hostname. In /etc/hosts we add the IP''s at the end of the file like, for eg:

```
192.168.0.101 pi1
192.168.0.102 pi2
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

To connect from one Pi to another, having followed only the above instructions, would require the following series of commands

```
$ ssh pi@192.168.0.10X
pi@192.168.0.10X's password: <enter password – 'raspberry' default>
```

Instead of the above approach we can use SSH aliases which facilitates easier and faster access

For this we have to edit the ~/.ssh/config file and add the following commands

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

```
ssh-keygen –t ed25519
```
This will generate a public / private key pair within the directory ~/.ssh/ which can be used to securely ssh without entering a password. One of these files will be called id_ed25519, this is the private key. The other, id_ed25519.pub is the public key.
The public key is used to communicate with the other Pis, and the private key never leaves its host machine and should never be moved or copied to any other device.

To overcome this problem each public key needs to be concatenated to the ~/.ssh/authorized_keys file on every other pi. 

On all other Pis run the following command:

```
$ cat ~/.ssh/id_ed25519.pub | ssh pi@192.168.0.101 'cat >> .ssh/authorized_keys'
```

This concatenates Pi #2's public key file to Pi #1's list of authorized keys, giving Pi #2 permission to ssh into Pi #1 without a password. We should also do this for Pi #1, so that when we copy the completed authorized_keys file to the other Pis, they all have permission to ssh into Pi #1, as well(assuming that Pi1 acts as the  master node).

```
$ cat .ssh/id_ed25519.pub >> .ssh/authorized_keys
```

Once this is done, as well as the previous section, ssh-ing is as easy as:

```

$ssh pi1

```
To replicate the passwordless ssh across all Pis, simply copy the two files mentioned above from Pi #1 to each other Pi using scp

```
$ scp ~/.ssh/authorized_keys piX:~/.ssh/authorized_keys
$ scp ~/.ssh/config piX:~/.ssh/config 
```

# Single Node(Master) set up Hadoop and Spark

## Bash Script of Master Node

All of the folowing needs to be edited on ~/.bashrc file

```
# To get hostname of other pis in the network
function otherpis {
        grep "pi" /etc/hosts | awk '{print $2}' | grep -v $(hostname) 
}

# To send commands to other pis in the network
function clustercmd {
        for pi in $(otherpis); do ssh $pi "$@"; done
        $@
}

# To send files to other pis
function clusterscp {
        for pi in $(otherpis); do
                cat $1 | ssh $pi "sudo tee $1" > /dev/null 2>&1
        done
}

# To restart all pis
function clusterreboot {
        clustercmd sudo shutdown -r now
}

# To shutdown all pis
function clustershutdown {
        clustercmd sudo shutdown now
}

# To copy the files in /opt/hadoop to all Pis
function copyconfig {
        for pi in $(otherpis); do rsync -avxP $HADOOP_HOME $pi:/opt; done
}

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-armhf
export HADOOP_HOME=/opt/hadoop
export SPARK_HOME=/opt/spark
export PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$PATH
export HADOOP_HOME_WARN_SUPRESS=1
```

## Set JAVA_HOME

* To find Java path, 
```
update-alternatives --display java
```
* Remove /bin/java - On Debian, the link is /usr/lib/jvm/java-11-openjdk-armhf/bin/java, so JAVA_HOME should be /usr/lib/jvm/java-11-openjdk-armhf.

* Update the hadoop-env.sh under ~/hadoop/etc/hadoop as: export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-armhf

## Hadoop installation

```
wget "https://archive.apache.org/dist/hadoop/common/hadoop-3.2.0/hadoop-3.2.0.tar.gz"
tar -xzf hadoop-3.2.0.tar.gz
sudo mv ~/hadoop-3.2.0 /opt/hadoop
```
We can use clustercp function to copy the same file across all the cluster so that hadoop is installed across all the nodes

After the above step change the permissions on the directory using :
```
$ sudo chown pi:pi -R /opt/hadoop
```

You can also verify if hadoop has been installed correctly by checking the version

```
$ cd && hadoop version | grep Hadoop

```
The output will be as follows

```
Hadoop 3.2.0
```

## Spark installation

```
wget "https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz"
tar -xzf spark-2.4.3-bin-hadoop2.7.tgz
sudo mv ~/spark-2.4.3-bin-hadoop2.7 /opt/spark
```

We can use clustercp function to copy the same file across all the cluster so that hadoop is installed across all the nodes

After the above step change the permissions on the directory using :
```
$ sudo chown pi:pi -R /opt/spark
```

You can also verify if hadoop has been installed correctly by checking the version

```
$ cd && spark version | grep spark

```
The output will be as follows

```
... version 2.4.3 ... Using Scala version 2.11.12 ...
```

## Versions of Hadoop and Spark

```
cd && hadoop version | grep Hadoop
cd && spark-shell --version
```

## HDFS

To get the Hadoop Distributed File System (HDFS) up and running, modify the following configuration files which are under /opt/hadoop/etc/hadoop.

1. Update core-site.xml file to set the NameNode location to Master on port 9000:
```
<configuration>

  <property>
  
    <name>fs.default.name</name>
    <value>hdfs://pi1:9000</value>
    
  </property>
  
</configuration>
```

2. To set path for HFDS, edit hdfs-site.xml. dfs.replication, indicates how many times data is replicated in the cluster. Set 4 to have all the data duplicated four nodes. Don’t enter a value higher than the actual number of worker nodes.
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

3. To set Yarn as Job Scheduler, edit mapred-site.xml, setting YARN as the default framework for MapReduce operations.
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

4. Edit yarn-site.xml, which contains the configuration options for YARN.
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

## Format HDFS

```
hdfs namenode -format -force
```

## Boot HDFS

* Start HDFS by running the following script from master node: 
```
start dfs.sh
```
* Start YARN with the following script from master node:
```
start yarn.sh
```

## Test HDFS

Check HDFS is working by creating a temporary directory

```
hadoop fs -mkdir /tmp
hadoop fs -ls /
jps
```

## Test Hadoop and Spark working together

```
hadoop fs -put $SPARK_HOME/README.md /
```

## Benchmark and Evaluation 

* Developed a test program (word count) to review Hadoop and Spark on Pi
* Time taken to burn SD card manually = 15 minutes
* Time taken to burn SD card using [cm-pi-burn](https://github.com/cloudmesh/cm-burn/blob/master/cm-pi-burn.py) = 3 minutes
* Time taken to download latest Raspbian image = 4 minutes
* Time taken to download latest Raspbian image using [cm-pi-burn](https://github.com/cloudmesh/cm-burn/blob/master/cm-pi-burn.py) = 2 minutes

## References

* <https://raspberrytips.com/install-raspbian-raspberry-pi/>
* <https://raspberrytips.com/raspberry-pi-cluster/>
* https://www.raspberrypi.org/documentation/remote-access/ip-address.md
* <https://dqydj.com/raspberry-pi-hadoop-cluster-apache-spark-yarn/>
* <https://www.mocomakers.com/building-a-raspberry-pi-cluster-with-apache-spark/>
* <https://tekmarathon.com/2017/02/16/hadoop-and-spark-installation-on-raspberry-pi-3-cluster-part-4/amp/>
* <https://medium.com/@glmdev/building-a-raspberry-pi-cluster-784f0df9afbd>
* <https://dev.to/awwsmm/building-a-raspberry-pi-hadoop-spark-cluster-8b2>
* <https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/>
* <https://www.linode.com/docs/databases/hadoop/install-configure-run-spark-on-top-of-hadoop-yarn-cluster/>
