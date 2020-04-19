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

# Usage
After running this application, a VXI11 server listens on the device for incoming connections.
Incoming connection requests to device names of the form "gpib,X" are mapped to gpib interface 0,
with primary address X.

A simple example using python-vxi11 could look like this:

```
import vxi11

instr = vxi11.Instrument("TCPIP::192.168.0.13::gpib,8::INSTR")

instr.write("*IDN?")
print(instr.read())
```
~                          
