#!/usr/bin/env python
__author__ = 'joshs@nyu.edu'

from netmiko import ConnectHandler
from ConfigParser import SafeConfigParser
from concurrent.futures import ThreadPoolExecutor
import argparse
import re
import sys
import validators

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("Error: %s\n" % message)
        self.print_help()
        sys.exit(2)

cparser = SafeConfigParser(allow_no_value=True)
cparser.read(['secret.conf', 'wlcs.conf'])
uname = cparser.get('secret', 'username')
pword = cparser.get('secret', 'password')

thread = ThreadPoolExecutor(max_workers=30)
wlcs = []
wlcs = cparser.options('wlcs')
d_routers = {}
routers = {}

aparser = MyParser()
aparser.add_argument('-m', '--mac', required=True, help="the mac address of the client")
aparser.add_argument('-a', '--action', required=True, choices=['block','unblock', 'search'], help="block, unblock or search")
aparser.add_argument('-c', '--comment', required=False, help="ticket information")

if len(sys.argv) == 1:
    print "Error: No arguments supplied\n"
    aparser.print_help()
    sys.exit(1)

args = aparser.parse_args()

if validators.mac_address(args.mac) is not True:
    print "Your MAC address appears invalid, closing"
    sys.exit(1)
elif args.action == "block" and not args.comment:
    print "You selected block but comment is missing, closing"
    aparser.print_help()
    sys.exit(1)
elif re.findall(r'unblock|search', args.action, re.IGNORECASE):
    args.comment = ""


def send_it(wlc, action, mac, comment):
    try:
        net_connect = ConnectHandler(**wlc)
    except Exception:
        err_output = "Error connecting to host: " + wlc['ip']
        print err_output

    if action == "block":
        command = "config exclusionlist add %s %s" % (mac, comment)
        output = net_connect.send_config_set([command, 'save config', 'y'])
        if output != "":
            if any(re.findall(r'error|incorrect', output, re.IGNORECASE)):
                print output
            elif "already exists" in output:
                print "Block of %s already exists on %s" % (mac, wlc['ip'])
            else:
                print "%s of %s on %s completed" % (action, mac, wlc['ip'])
    elif action == "unblock":
        command = "config exclusionlist delete %s" % (mac)
        output = net_connect.send_config_set([command, 'save config', 'y'])
        if "Deleted exclusion-list entry" in output:
            print "%s of %s on %s completed" % (action, mac, wlc['ip'])
        else:
            print "Error %sing of %s on %s. \nThis is probably due to the block not existing, try searching instead" % (action, mac, wlc['ip'])
    elif action == "search":
        command = "show exclusionlist"
        output = net_connect.send_command(command)
        if re.search(mac, output, re.IGNORECASE):
            print "MAC address %s is blocked on controller with ip %s" % (mac, wlc['ip'])
        else:
            print "MAC address %s is NOT blocked on controller with ip %s" % (mac, wlc['ip'])

    net_connect.disconnect()



for wlc in wlcs:
    routers[wlc] = {
        'device_type' : 'cisco_wlc_ssh',
        'ip' : wlc,
        'username' : uname,
        'password' : pword,
        'timeout' : 15,
    }
    output = thread.submit(send_it, routers[wlc], args.action, args.mac, args.comment)