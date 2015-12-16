#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
# sys.path.insert(0, "/home/christophe/Documents/Projects/programming_projects/rq")
sys.path.insert(0, "/home/christophe/workspace/velona/rq")

from time import sleep
import signal
import os
import psutil

from rq import Worker

from rqtest.functions import wait_a_bit
from redis import Redis
from rq import Queue


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
    try:
        pid = worker_name.split('.')[1]
        os.kill(int(pid), signal.SIGTERM)
    except OSError:
        print('process does not exist')
    except Exception as e:
        print("Error canceling worker: %s" % e)
        raise


def kill_worker_evil(worker_name):
    try:
        pid = worker_name.split('.')[1]
        os.kill(int(pid), signal.SIGTERM)
        sleep(0.5)
        os.kill(int(pid), signal.SIGTERM)
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


def workersrq():
    workers = []
    for worker in Worker.all(connection=conn1):
        workers.append(worker.name)
        print(worker.name, worker.state)
    if len(workers) == 0:
        print("No WORKERS!!!")
        return None
    else:
        return workers[0]

"""
TEST
(remember to launch a worker with ./launchworker.py)
"""
print("\nSTART\n")
print('* Running before job (RQ)')
worker_name = workersrq()
print('* Running before job (PS)')
workerprocs()

job = q.enqueue(wait_a_bit, 10)
print('Enqueued', job)

sleep(1)

print('* Running with job ongoing (RQ)')
workersrq()
print('* Running  with job ongoing (PS)')
workerprocs()

"""
A new process appears with same commandline and new pid
"""

print('SENDING SIGNAL NOW')
"""
kill_worker_gently:
Trying with first via RQ, then os.lill SIGKILL --> redis is empty at once?
Trying other way around --> OK!!!
"""

"""
kill_worker_evil:
Trying with twice SIGTERM with sleep in btw --> OK
Trying the same but with a kill gentyly signal before --> OK
Adding lots of kill signals --> OK, no exception
Trying with two kill gentlies in a row --> no?
Adding a sleep between the two in kill evil is ok. Using kill evil wihtou sleep is no tok ??
Using kill gently twice is ok again. So a bit of time between the two signals is necesary
"""
print('* Running in between signals (RQ)')
workersrq()
print('* Running  in between signals (PS)')
workerprocs()
kill_worker_evil(worker_name)

print('* Running after, with job ongoing (RQ)')
workersrq()
print('* Running after, with job ongoing (PS)')
workerprocs()

sleep(2)
print('* Running after, with job finished (RQ)')
workersrq()
print('* Running after, with job finished (PS)')
workerprocs()

print("\nEND\n")
