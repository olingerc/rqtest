#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
sys.path.insert(0, "/home/christophe/Documents/Projects/programming_projects/rq")

from time import sleep

from rqtest.functions import wait_a_bit
from redis import Redis
from rq import Queue
from rq.registry import StartedJobRegistry

"""
Test enqueing a job but deleting it before it has finished. The reason is to Test
that the job is correctly remove from the redis StartedJobRegistry
"""

conn = Redis('localhost', 6379)

q = Queue(connection=conn)
job = q.enqueue(wait_a_bit, 10)
registry = StartedJobRegistry(job.origin, conn)

print('Enqueued', job)
sleep(2)

print('StartedJobRegistry, before delete:')
print(registry.get_job_ids())

job.delete()

print('StartedJobRegistry, after delete:')
print(registry.get_job_ids())
