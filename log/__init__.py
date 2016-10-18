#! /usr/bin/python3
# -*- coding: utf-8 -*-

'''
      Copyright 2016,暗夜幽灵 <darknightghost.cn@gmail.com>

      This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    at your option) any later version.

      This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

      You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import time

enable_logging = False

def logging_on():
    global enable_logging
    enable_logging = True
    return

def logging_off():
    global enable_logging
    enable_logging = False
    return

def write_log(filename, logstr):
    timestr = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    logline = "%s : %s"%(timestr, logstr)
    os.system("echo \"%s\" >> %s"%(logline, filename))
    return

def debug_log(logstr):
    global enable_logging
    if enable_logging:
        write_log("./debug.log", logstr)


