#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
from tornado.options import options, define
import sys
import os
import time
import json
import pssh
import logging
import tempfile

define("config", type=str, metavar="config.py",
        callback=lambda path: options.parse_config_file(path, final=False),
        help="config file (optional)")
define("hosts", type=str, multiple=True,
        metavar="host1,host1,...",
        help="comma-separated list of ssh hosts (required or specify hosts-file)")
define("hosts_file", type=str, multiple=False,
        metavar="hostfile.txt",
        help="file containing new-line separated list of ssh hosts (required or specify hosts)")
define("command", type=str, metavar="uptime", help="command to execute on hosts (required)")
define("outdir", type=str, metavar="/tmp", default=os.getcwd(), help="output directory")
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
    options.logging = 'warn'
    options.add_parse_callback(validate_options)
    options.parse_command_line()
    if not os.path.exists(options.outdir):
        os.mkdir(options.outdir)
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
        fn = '{}_{}'.format(host, time.strftime("%Y_%m_%d_%H%M%S", time.gmtime()))
        with open(os.path.join(options.outdir, fn), 'w') as fh:
            fname = fh.name
            for line in response[host]['stdout']:
                logger.info('[{}][{}]: {}'.format(host, retval, line))
                fh.write(line)
                fh.write('\n')
        host_responses[host] = { 'exit_code': retval, 'stderr': stderr, 'stdout_file': fname }
    non_zero = []
    for h in host_responses.keys():
        if host_responses[h]['exit_code'] != 0:
            non_zero.append(h)
    json.dump({'hosts': host_responses,
            'non_zero': non_zero}, sys.stdout)
