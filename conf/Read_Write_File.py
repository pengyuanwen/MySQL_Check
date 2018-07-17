#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Handler_file(object):

    def __init__(self,files):
        self.files = files

    def Read_File(self):
        with open(self.files, 'r') as file:
            res = file.readlines()
            return res

    def Write_File(self,data):
        with open(self.files,'w') as file:
            res = file.write(data)
            return res