#!/usr/bin/env python
__author__ = 'joshs@nyu.edu'

from netmiko import ConnectHandler

net_connect = ConnectHandler(device_type='cisco_wlc', ip='10.10.10.227', username='', password='')
output = net_connect.send_command("show exclusionlist")
print output