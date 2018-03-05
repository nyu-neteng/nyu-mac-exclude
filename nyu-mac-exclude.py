#!/usr/bin/env python
__author__ = 'joshs@nyu.edu'

from netmiko import ConnectHandler
from ConfigParser import SafeConfigParser
import argparse
import re

aparser = argparse.ArgumentParser("Blocks/Unblocks a MAC address on the WLCs. Format is \"nyu-mac-exclude.py <macaddress> <block,unblock> <ticket# as description>\"")
aparser.add_argument("mac", help="the mac address of the client to block")
aparser.add_argument("action", choices=['block','unblock'], help="block or unblock")
aparser.add_argument("description", help="ticket information")

args = aparser.parse_args()

cparser = SafeConfigParser(allow_no_value=True)
cparser.read(['secret.conf', 'wlcs.conf'])
uname = cparser.get('secret', 'username')
pword = cparser.get('secret', 'password')

def send_command(mac, action, description, wlc, uname, pword):
    try:
        net_connect = ConnectHandler(device_type='cisco_wlc', ip=wlc, username=uname, password=pword, timeout=15)
    except Exception:
        err_output = "Error connecting to host: " + wlc
        return err_output

    command = "config exclusionlist %s %s %s" % (action, mac, description)
    #print command
    output = net_connect.send_config_set([command, 'save config', 'y'])

    return output


wlcs = {}
wlcs = cparser.options('wlcs')

for wlc in wlcs:
    if args.action == "block":
        output = send_command(args.mac, "add", args.description, wlc, uname, pword)
    elif args.action == "unblock":
        output = send_command(args.mac, "delete", "", wlc, uname, pword)

    if output != "":
        if any(re.findall(r'error|incorrect|already exists', output, re.IGNORECASE)):
            print output
        else:
            print "Added block of %s to %s" % (args.mac, wlc)