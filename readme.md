parssh
======

Another parallel ssh command executor

*WIP - need to add gevent support to paramiko for full functionality & performance* 

Command line wrapper for [pkittenis/parallel-ssh](https://github.com/pkittenis/parallel-ssh).

Powered by:
* [python](https://www.python.org/)
* [gevent](http://www.gevent.org/contents.html)
* [paramiko](https://github.com/paramiko/paramiko)
* [torando.options](http://tornado.readthedocs.org/en/latest/options.html)

usage

```
% ./parssh.py --help
Usage: ./parssh.py [OPTIONS]

Options:

  --command=uptime                 command to execute on hosts (required)
  --config=config.py               config file (optional)
  --help                           show this help information
  --hosts=host1,host1,...          comma-separated list of ssh hosts (required
                                   or specify hosts-file) (default [])
  --hosts_file=hostfile.txt        file containing new-line separated list of
                                   ssh hosts (required or specify hosts)
  --sudo                           use sudo (default False)

/opt/virtualenvs/parssh/lib/python2.7/site-packages/tornado/log.py options:

  --log_file_max_size              max size of log files before rollover
                                   (default 100000000)
  --log_file_num_backups           number of log files to keep (default 10)
  --log_file_prefix=PATH           Path prefix for log files. Note that if you
                                   are running multiple tornado processes,
                                   log_file_prefix must be different for each
                                   of them (e.g. include the port number)
  --log_to_stderr                  Send log output to stderr (colorized if
                                   possible). By default use stderr if
                                   --log_file_prefix is not set and no other
                                   logging is configured.
  --logging=debug|info|warning|error|none
                                   Set the Python log level. If 'none', tornado
                                   won't touch the logging configuration.
                                   (default info)
```
