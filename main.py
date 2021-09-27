#!/usr/bin/python3

import sys
import json
import pexpect
from pexpect import EOF
from func import removeDup

begin = '(0x(B [93m'

evil = pexpect.spawn('sudo evillimiter --flush', timeout=None)
evil.logfile = sys.stdout.buffer

evil.expect('>>>')
evil.sendline('scan')
evil.expect('>>>')
evil.sendline('hosts')
evil.expect('>>>')

hosts: str = evil.before.decode('utf-8')

hostsL: list[str] = hosts.splitlines()

whitelistF = open('whitelist.txt', '+r')
whitelist = whitelistF.read()
whitelistF.close()

whitelistL: list[str] = whitelist.splitlines()

resourceF = open('resource.txt', '+r')
resource = resourceF.read()
resourceF.close()

data: list[dict[str, str]] = json.loads(resource)

WLID: list[str] = []

for line in hostsL:
    if line.startswith(begin):
        id = line[13:15].strip('')
        mac = line[51:69].strip(' ')
        ip = line[28:44].strip('').strip(' ')

        data.append({mac: ip})

        for white in whitelistL:
            if white == mac:
                WLID.append(id)

freeCmd = 'free {}'.format(','.join(WLID))

data = removeDup(data)
data = sorted(data, key=lambda k: list(k.values())[0])
dataJson = json.dumps(data, indent=2)

resourceF = open('resource.txt', '+w')
resource = resourceF.write(dataJson)
resourceF.close()

evil.sendline('block all')
evil.expect('>>>')
evil.sendline(freeCmd)
evil.expect(EOF)
