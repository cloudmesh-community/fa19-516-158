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

To enable user-defined, static IP addresses, edit the file /etc/dhcpcd.conf on each Pi and uncomment/edit the lines:

```
interface eth0
static ip_address=192.168.0.10X/24
```
where, X denotes the number to be assigned for every Pi. After this change has been made on a particular Pi, reboot the machine. Once this is done for all Pis in the network, they should all be able to ping each other at those addresses.

## Set password, Enable SSH and Reboot Pi

```
sudo su
passwd
sudo passwd pi
sudo raspi-config
sudo systemctl enable ssh
sudo systemctl start ssh
sudo reboot
```

## Single Node(Master) set up

The following files need to be changed as follows:

* core-site.xml

```
<configuration>
        <property>
                <name>fs.defaultFS</name>
                <value>hdfs://pi1:9000</value>
        </property>
</configuration>
```

* hdfs-site.xml

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
                <value>1</value>
        </property>

</configuration>
```

* mapred-site.xml

```
<configuration>
        <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
        </property>
</configuration>
```

* yarn-site.xml

```
<configuration>

<!-- Site specific YARN configuration properties -->

        <property> 
                <name>yarn.nodemanager.aux-services</name>
                <value>mapreduce_shuffle</value>
        </property>

        <property>
                <name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>
                <value>org.apache.hadoop.mapred.ShuffleHandler</value>
        </property>

</configuration>
```
