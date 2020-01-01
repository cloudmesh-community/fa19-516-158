# Hadoop Clusters With Raspberry Pi

*Disclaimer: The writeup provided here only includes some theoretical
notes. They were not implemented on a Raspberry Pi. Furthermore, this
project and the analysis of the scripts do not leverage Cloudmesh,
which makes the task for interacting with a cluster much easier. We
keep this section as it could provide some useful information for
future students searching for a project. 

Furthermore, Gregor von Laszewski and Sub have significantly
contributed to the implementation of the pi burn code. The report has
been significantly updated by Gregor von Laszewski to provide guidance
for others on how to proceed.*

* Gregor von Laszewski
* Daivik Uggehalli Dayanand, [fa19-516-158](https://github.com/cloudmesh-community/fa19-516-158)
* Akshay Kowshik, [fa19-516-150](https://github.com/cloudmesh-community/fa19-516-150)
* Insights: <https://github.com/cloudmesh-community/fa19-516-158/graphs/contributors>
* Project Directory (not operational): <https://github.com/cloudmesh-community/fa19-516-158/tree/master/project> 
* Code: <https://github.com/cloudmesh/cm-burn/blob/master/cmburn/> 
* Host: <https://github.com/cloudmesh/cloudmesh-inventory/tree/master/cloudmesh/host> (developed by Gregor von Laszewski)
* Manual (mostly developed by von Laszewski): <https://github.com/cloudmesh/cloudmesh_pi_burn/blob/master/cm-pi-burn.md>

## Introduction

According to von Laszewski, the Raspberry Pi provides the community with
a cheap platform with the ability to expose Linux and other operating
systems to the masses. Due to its cost point, it is easy to buy a PI and
experiment with it. As such, this platform has been ideal for lowering
the entry barrier to advanced computing from the university level to
high school, middle school, and even elementary school. However, the PI
has also been used by universities and even national labs. Due to its
availability and its convenient accessibility, it has become a staple of
our educational pipeline. Due to its price point, the PI can also be
used to build cheap clusters putting forward a hardware platform ideal
for experimenting with issues such as networking and cluster management
as an educational tool. Many such efforts exist to use a PI as a cluster
environment.

So it would be a good idea if we could turn such a platform more
powerful by deploying the latest technologies such as Hadoop and Spark on
It. Multi cluster Raspberry Pi, where one node can act as the master
node and other nodes act like workers, and the master might be able to
control the workers.

## Architecture

The deployment of Hadoop on Raspberry Pi Clusters involves the
preparation of the cluster. This includes

* Using `cm-pi-burn` command to burn multiple SD cards at once
* (incomplete) Creating a cluster with as many nodes as we have SD cards for

Once we have a cluster, a master node maintains knowledge about the
distributed file system and schedules resource allocation. It hosts two
daemons (:o2: this is unclear, from where are these deomons comming.):

1. :o2: The NameNode manages the distributed file system and knows where
   stored data blocks inside the cluster are.
2. :o2: The ResourceManager manages the YARN jobs and takes care of
   scheduling and executing processes on worker nodes.

The worker nodes store the actual data and provide processing power to
run  the jobs and host two daemons:

1. The DataNode manages the physical data stored on the node; it is
   named, NameNode.
2. The NodeManager manages execution of tasks on the node.

## Technologies used

To achieve this, we use the following technologies

* cloudmesh common
* cloudmesh-inventory
* cloudmesh-cloud
* cm-burn
* Python
* HDFS
* Hadoop


## Implementation

:o2: AN introduction is missing that deliniates the burn from the
deployment process.

(:o2: the implementation is not completed) The implementation consists
of the following steps:

1. Buring the Raspian image on the SD card
2. Setting Static IP address on the SD card
3. Setting HostNames on the SD card

Due to the use of `cm-pi-burn`, the cluster SD Cards come preinstalled
with hostnames, IP addresses, user key, and ssh enabled, so accessing
each pi is easy and possible immediately after the boot. See the
[cm-pi-burn](<https://github.com/cloudmesh/cloudmesh_pi_burn/blob/master/cm-pi-burn.md>)
manual for guidance on how to conduct these steps.

**DISCLAIMER: THE NEXT STEPS HAVE NOT BEEN TESTED AND DO NOT LEVERAGE
*CLOUDMESH NOR DO THEY DISCUSS HOW THEY CAN USE CLOUDMESH TO SIMPLIFY
*THE TASK. WE NEED TO MAKE SURE YOU UNDERSTAND THIS IMPORTANT
*RESTRICTION. AT THIS TIME THIS PROJECT IS INCOMPLETE AS IT LACKS A
*PROPER ANALYSIS HOW TO LEVERAGE CLOUDMESH AND TO CONDUCT THE
*DEPLOYMENT. THE METHOD DISCUSSED HERE IS COPIED FROM THE INTERNET
*WITHOUT VERIFICATION. LINKS TO THESE DOCUMENTS ARE PROVIDED IN THE
*REFERENCE SECTION BUT ARE NOT USED IN THE TEXT, WHICH IS TYPICALLY NOT
*DONE AS PROPER CREDIT AND CITATION  IS IMPORTANT.**


The solutions published in the Web include the use of bash scripts for
the deployment. However, Cloudmesh provides much better features while
providing host management and an inventory. The cluster command and
deployment that this project was supposed to implement was not
completed.


The remaining steps include (:o2: spark is not mentioned)

4. creating passwordless keys and distributing it to all hosts 
5. Downloading Hadoop on the master node 
6. Copying the Hadoop files from the master node across the cluster of n7odes using SCP
6. Changing the Configuration Files of Hadoop to set the replication factor, NameNode location

 To create passwordless keys and to distribute them to all hosts,  you can simply call the `cms host` command and execute the ssh-keygen command on all PIs (note we need to verify that the host command works). After that, we can use the host command to fetch all keys, merge them in a
 single `authorized_keys` file, and upload them to all of the pis. This makes it now possible to login between each pi.  Naturally, we have
 also added our local key, so we do not lose access from our laptop

The following functionality is needed for the cluster command

* copy files between all or selected nodes
* copy files onto all or selected nodes
* reboot an all or selected nodes
* shutdown on all or selected nodes

As we use Cloudmesh these commands are trivial to implement and
constitute a one-line implementation.

## Hadoop installation

In this section, we discuss theoretically how to installing Hadoop 3.2.0
into a directory called `/opt/hadoop`. However, we have not tried this.

```
wget "https://archive.apache.org/dist/hadoop/common/hadoop-3.2.0/hadoop-3.2.0.tar.gz"
tar -xzf hadoop-3.2.0.tar.gz
sudo mv ~/hadoop-3.2.0 /opt/hadoop
```

Here we would then use the Cloudmesh cluster or host command to copy the
same file across all the cluster so that Hadoop is installed across all
the nodes.


In addition we need to assamble a customized `.bashrc` file that is than
populated on all nodes. The add on to the .bashrc file includes:


```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-armhf
export HADOOP_HOME=/opt/hadoop
export SPARK_HOME=/opt/spark
export PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$PATH
export HADOOP_HOME_WARN_SUPRESS=1
```

## Install Java

:o2: This section is incomplete and not properly documented while providing
an easy to use a script. Instead we only provide some initial pointers on
how to derive such a script.

* To find Java path

```bash
update-alternatives --display java
```

* Remove /bin/java - On Debian, the link is

  /usr/lib/jvm/java-11-openjdk-armhf/bin/java, so JAVA_HOME should be
  /usr/lib/jvm/java-11-openjdk-armhf.

* Update the hadoop-env.sh under ~/hadoop/etc/hadoop as:

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-armhf
```
After the above step change the permissions on the directory using:

```bash
$ sudo chown pi:pi -R /opt/hadoop
```

You can also verify if Hadoop has been installed correctly by checking
the version

```
$ cd && hadoop version | grep Hadoop
```

The output will be

```
Hadoop 3.2.0
```

## Install HDFS

:o2: This section does not provide a script to conduct the HDFS. Instead
we provide some very initial pointers on how one could develop such a
script while listing some of the steps. The templates provided here
should be included in our cluster deployment form while using the python
format statement to modify the parameters and write them to files that
than can be used in the deployment.


To get the Hadoop Distributed File System (HDFS) up and running one
needs to modify the following configuration files which are under

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

2. To set the path for HFDS, change the hdfs-site.xml. dfs.replication, indicates
   how many times data is replicated in the cluster. Set 4 to have all the data duplicated four nodes. Don’t enter a value higher than the actual
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

These files need to be placed in  `/opt/hadoop`

with a command you start from cloudmesh using rsync

:o2: this needs to be done with cloudmesh

```bash rsync -avxP $HADOOP_HOME $pi:/opt; done } ``` 

Once this is
achieved you need to format HDFS with (here the documentation is unclear
as it is not stated if it is done on all or just the master node).


```bash
$ hdfs namenode -format -force
```

Next, you Start HDFS and yarn by running the following script from the master
node:

```bash
$ start dfs.sh
$ start yarn.sh
```

## Test HDFS

Check HDFS is working by creating a temporary directory.

```bash
$ hadoop fs -mkdir /tmp
$ hadoop fs -ls /
$ jps
```
## Spark installation

The spark installation is very similar to the Hadoop installation

```bash
$ wget "https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz"
$ tar -xzf spark-2.4.3-bin-hadoop2.7.tgz
$ sudo mv ~/spark-2.4.3-bin-hadoop2.7 /opt/spark
```

On each node (unclear from previous description) you need

```bash
$ sudo chown pi:pi -R /opt/spark
```

Add the following 2 environment variables to the .bashrc file:

```
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH
```

Create the Spark configuration file and add the following lines at the
end of the config file:

```
$ cd $SPARK_HOME/conf
$ sudo mv spark-defaults.conf.template spark-defaults.conf
```

```
spark.master            yarn
spark.driver.memory     465m
spark.yarn.am.memory    356m
spark.executor.memory   465m
spark.executor.cores    4
```

You can  verify if Spark has been installed correctly by checking
the version

```bash
$ cd && spark version | grep spark

```

The output will be as follows.

```
... version 2.4.3 ... Using Scala version 2.11.12 ...
```

#### Test Hadoop and Spark working together

```bash
$ hadoop fs -put $SPARK_HOME/README.md /
```

#### Versions of Hadoop and Spark

```bash
$ cd && hadoop version | grep Hadoop
$ cd && spark-shell --version
```

#### Test if Spark works on Pi

spark-shell opens the ```scala>``` command line 

```
scala> object HelloWorld {
    |   def main(args: Array[String]): Unit = {
    |     println("Hello, world!")
    |   }
    | }
defined module HelloWorld

scala> HelloWorld.main(Array())

Hello, world! # Output displayed

scala>:q
>
```
## Benchmarks

This project lacks the proper report of benchmarks. We also believe the
benchmark is not properly reported as it does not measure the time to
add the information by hand.

The benchmarks for our project was to record the time it normally takes
to burn a single SD card and do all the setup part versus the time it
takes to burn one SD card using cm-burn automatically with Static IP and
hostname set to it. Any cm-pi-burn help commands can be used with a -v
flag along with to display the results along with the timings. For eg 

```
cm-pi-burn [-v] create [--image=IMAGE] \
           [--device=DEVICE] \
           [--hostname=HOSTNAME] \
           [--ipaddr=IP] \
           [--sshkey=KEY] \
           [--blocksize=BLOCKSIZE] \
           [--dryrun]
```           

will display the results along with the time it takes to burn an image
along with Ip address and hostname set along with it.
 
The results can be summarised as follows:

:o2: We do not believe these benchmark numbers as it will take much more
time to set up the information by hand. the first time.

:o2: THe benchmark is done with the assumption that an expert sets it up,
however cm-pi-burn needs no expert.

Manual burn: 8-9 minutes to burn one SD card and set up a static IP and
hostname to it

cm-pi-burn : 420 seconds(6 minutes) to burn 2 SD cards

cm-pi-burn turns out to be very much efficient as compared to the Naive approach

## Acknowledgements

The previous report did not make it clear that the Spark and Hadoop
setup have not been tested. This has been corrected, and the incomplete
nature of this work has now been correctly reported so that others can pick up this project and complete it.

## References

:o2: refernces should be done in bibtex

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
