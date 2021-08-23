# Author: gh0stxplt
#
# Date: 08/13/2021
#
#!/usr/bin/env python3

import subprocess

interface = input("Interface > ")
usrMAC = input("MAC Address > ")

print("[+] Changing MAC Address for interface " + interface + " to MAC " +
      usrMAC)

subprocess.call(["ifconfig", interface, "down"])

subprocess.call(["ifconfig", interface, "hw", "ether", usrMAC])

subprocess.call(["ifconfig", interface, "up"])
