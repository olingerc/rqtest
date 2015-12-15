#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
sys.path.insert(0, "/home/christophe/Documents/Projects/programming_projects/rq")

from time import sleep
import signal
import os
import psutil

from rq import Connection, Worker

from rqtest.functions import wait_a_bit
from redis import Redis
from rq import Queue
from rq.registry import StartedJobRegistry

"""
Test deleting workers warm and cold
"""

conn1 = Redis('localhost', 6379)
worker_name = None
q = Queue(connection=conn1)

"""
FUNCS
"""


def kill_worker_gently(worker_name):
    with Connection(connection=conn1):
        for worker in Worker.all():
            if worker.name == worker_name:
                worker.register_death()
    try:
        pid = worker_name.split('.')[1]
        # TODO: check rq, worker.pid not correct ?!
        os.kill(int(pid), signal.SIGTERM)
        # TODO: handle time btw shot and death inform client
    except OSError:
        print('process does not exist')
    except Exception as e:
        print("Error canceling worker: %s" % e)
        raise


def kill_worker_evil(worker_name):
    with Connection(connection=conn1):
        for worker in Worker.all():
            if worker.name == worker_name:
                worker.register_death()
    try:
        pid = worker_name.split('.')[1]
        # TODO: check rq, worker.pid not correct ?!
        # TODO: kill subprocesses, change mongo status of running job
        os.kill(int(pid), signal.SIGKILL)
    except OSError:
        print('process does not exist')
    except Exception as e:
        print("Error killing worker: %s" % e)
        raise

def workerprocs():
    for proc in psutil.process_iter():
        try:
            if "launchworker.py" in str(proc.cmdline()):
                print(proc.cmdline(), proc.pid)
        except psutil.NoSuchProcess:
            pass

"""
TEST
(remember to launch a worker with ./launchworker.py)
"""
print("\nSTART\n")
print('* Running before job (RQ)')
for worker in Worker.all(connection=conn1):
    if worker_name is None:
        worker_name = worker.name
    print(worker.name)

print('* Running before job (PS)')
workerprocs()

job = q.enqueue(wait_a_bit, 2)
print('Enqueued', job)

sleep(1)

print('* Running with job ongoing (RQ)')
for worker in Worker.all(connection=conn1):
    print(worker.name, worker.state)

print('* Running  with job ongoing (PS)')
workerprocs()

"""
A new process appears with same commandline and new pid
"""

print('SENDING SIGNAL NOW')

sleep(2)

print('* Running after, with job finished (RQ)')
for worker in Worker.all(connection=conn1):
    print(worker.name, worker.state)

print('* Running after, with job finished (PS)')
workerprocs()

print("\nEND\n")
