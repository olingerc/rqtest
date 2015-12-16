#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
# sys.path.insert(0, "/home/christophe/Documents/Projects/programming_projects/rq")
sys.path.insert(0, "/home/christophe/workspace/velona/rq")

from rq import Connection, Worker, Queue
from redis import Redis


# Redis connections
conn1 = Redis()

'''Queues should be comma separated list
   e.g. python launch_worker.py single,long
   default:
'''

listen = ['default']
if len(sys.argv) > 1:
    listen = [x.strip() for x in sys.argv[1].split(',')]

if __name__ == '__main__':
    with Connection(connection=conn1):
        w = Worker(map(Queue, listen))
        w.work()
