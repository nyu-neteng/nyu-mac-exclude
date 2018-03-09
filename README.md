# nyu-mac-filter

This script communicates with a list of Cisco WLC devices via ssh and adds a MAC address to the exclusion list on each
controller to block the host from gaining wireless access to the network.

**Requirements**
1. Copy wlcs.conf.example to wlcs.conf and add ip's of WLC devices.
2. Copy secrets.conf.example to secrets.conf and add account information for ssh. If using RBAC, account must be member
   of SECURITY group or higher.

For python requirements, use the requirements.txt file.
```shell
pip install -r requirements.txt
```

## Usage

***To block host FF:FF:FF:FF:FF:FF***
```shell
./nyu-mac-exclude.py -m FF:FF:FF:FF:FF:FF -a block -c "Comment required"

block of FF:FF:FF:FF:FF:FF on 1.1.1.1 completed
```
***To unblock host FF:FF:FF:FF:FF:FF***
```shell
./nyu-mac-exclude.py -m FF:FF:FF:FF:FF:FF -a unblock

unblock of FF:FF:FF:FF:FF:FF on 1.1.1.1 completed
```
***See if host FF:FF:FF:FF:FF:FF is currently blocked***
```shell
./nyu-mac-exclude.py -m FF:FF:FF:FF:FF:FF -a search

MAC address FF:FF:FF:FF:FF:FF is blocked on controller with ip 1.1.1.1
```
or
```
MAC address FF:FF:FF:FF:FF:FF is NOT blocked on controller with ip 1.1.1.1
```

## License
This project is published with the <a href="https://opensource.org/licenses/MIT" target="_blank">MIT license</a>.