#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Handler_file(object):

    def __init__(self,files):
        self.files = files

    def Read_File(self):
        with open(self.files, 'r') as f:
            res = f.readlines()
            return res

    def Write_File(self,data):
        with open(self.files,'w') as f:
            res = f.write(data)
            return res