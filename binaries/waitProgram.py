#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from time import sleep
import re


find = re.compile(r'[0-9]{3}.[0-9]{2}.[0-9]{2}.[0-9]([0-9]+)')

res = find.findall(argv[1])
if len(res) == 1:
    dat = int(res[0])
    print(dat)
    sleep(dat) 





