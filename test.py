#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
sys.path.insert(0, "/home/christophe/Documents/Projects/programming_projects/rq")
from rqtest.function import wait_a_bit

from redis import Redis
from rq import Queue

q = Queue(connection=Redis())


result = q.enqueue(wait_a_bit, 3)
print(result)
