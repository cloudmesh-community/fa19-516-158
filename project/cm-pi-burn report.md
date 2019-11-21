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


