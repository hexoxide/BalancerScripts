#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys; 

def getInput(inp):
    if sys.version_info[0] < 3:
        return raw_input(inp)
    else:
        return input(inp)
