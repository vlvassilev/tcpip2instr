## VXI11 TCP/IP to GPIB gateway
This piece of software implements funcionality comparable to a Ethernet-to-GPIB bridge.
It uses coburnw's python-vxi11-server and the linux-gpib python bindings. Currently,
only read and write methods are supported, though it can be easily extended.
Uses python2 because of reasons.

# Installation
Starting from a working gpib configuration and linux-gpib available in python, the following
commands can be used for installation on a Debian-like system with systemd.

```
sudo apt-get install rpcbind
sudo systemctl start rpcbind
sudo systemctl enable rpcbind

git clone https://github.com/coburnw/python-vxi11-server.git
git clone https://git.loetlabor-jena.de/thasti/tcpip2instr.git
cd tcpip2instr
python tcpip2instr.py
```
