#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-10 15:13:31 armin>

import os

def getfiles(dir):
    for file in os.listdir(dir):
        if os.path.isdir(file):
            print file
            getfiles(file)
        else:
            print file
    
    
def listdir(dir):
    return     
    

if __name__ == "__main__":
    getfiles(u"/home/armin/code")