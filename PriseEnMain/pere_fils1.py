# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 09:21:15 2021

@author: romai
"""

import os

print(os.getpid())
pid = os.fork()
print(pid)
