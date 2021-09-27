#!/usr/bin/python3

import sys
import pexpect
from pexpect import EOF

begin = '(0x(B [93m'

evil = pexpect.spawn('sudo evillimiter --flush', timeout=None)
evil.logfile = sys.stdout.buffer

evil.expect('>>>')
evil.sendline('scan')
evil.expect('>>>')
evil.sendline('hosts')
evil.expect('>>>')

hosts: str = evil.before.decode('utf-8')

#
# hostsF = open('hosts.txt', '+r')
# hosts = hostsF.read()
# hostsF.close()
#

hostsL: list[str] = hosts.splitlines()

whitelistF = open('whitelist.txt', '+r')
whitelist = whitelistF.read()
whitelistF.close()

whitelistL: list[str] = whitelist.splitlines()

ID: list[str] = []
IP: list[str] = []
MAC: list[str] = []
WLID: list[str] = []

for line in hostsL:
    if line.startswith(begin):
        id = line[13:15].strip('')
        mac = line[52:69]
        ID.append(id)
        MAC.append(mac)
        IP.append(line[28:44].strip())

        for white in whitelistL:
            if white == mac:
                WLID.append(id)

freeCmd = 'free ' + ','.join(WLID)

evil.sendline('block all')
evil.expect('>>>')
evil.sendline(freeCmd)
evil.expect(EOF)
