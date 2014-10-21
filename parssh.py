#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
from tornado.options import options, define
import sys
import os
import json
import pssh
import logging

define("config", type=str, metavar="config.py",
        callback=lambda path: options.parse_config_file(path, final=False),
        help="config file (optional)")
define("hosts", type=str, multiple=True,
        metavar="host1,host1,...",
        help="comma-separated list of ssh hosts (required or specify hosts-file)")
define("hosts_file", type=str, multiple=False,
        metavar="hostfile.txt",
        help="file containing new-line separated list of ssh hosts (required or specify hosts)")
define("command", type=str, metavar="uptime",
        help="command to execute on hosts (required)")
define("sudo", type=bool, default=False, help="use sudo")

def validate_options():
    if not options.command:
        options.print_help()
        raise Error('missing required command option')
    if not options.hosts and not options.hosts_file:
        options.print_help()
        raise Error('missing required option hosts or hosts-file')

class Error(Exception):
    pass

if __name__ == '__main__':
    try:
        options.logging = 'warn'
        options.add_parse_callback(validate_options)
        options.parse_command_line()
    except Error as e:
        sys.stderr.write('{}\n'.format(str(e)))
    logger = logging.getLogger()
    if options.hosts_file:
        with open(options.hosts_file) as file:
            hosts = [ l.strip() for l in file.readlines() ]
    client = pssh.ParallelSSHClient(hosts, pool_size=50)
    greenlets = client.exec_command(options.command, sudo=options.sudo)
    host_responses = {}
    for g in greenlets:
        response = client.get_stdout(g, return_buffers=True)
        host = response.keys().pop()
        retval = response[host]['exit_code']
        stderr = [line for line in response[host]['stderr']]
        for line in response[host]['stdout']:
            logger.info('[{}][{}]: {}' .format(host, retval, line))
        host_responses[host] = { 'exit_code': retval, 'stderr': stderr }
    non_zero = []
    for h in host_responses.keys():
        if host_responses[h]['exit_code'] != 0:
            non_zero.append(h)
    json.dump({'hosts': host_responses,
            'non_zero': non_zero}, sys.stdout)
