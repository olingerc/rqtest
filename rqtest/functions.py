#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import time

def wait_a_bit(waitfor):
    time.sleep(waitfor)
    print('waited for %s seconds' % waitfor)
    return 'done'
