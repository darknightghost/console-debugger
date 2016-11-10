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

from adapters.functions import *

class Adapter:
    def __new__(cls, *args, **kwargs):
        if "_instance" not in Adapter.__dict__:
            Adapter._instance = object.__new__(cls)
            cls.initialized = False

        return Adapter._instance

    def __init__(self, cfg, param_dict):
        if type(self).initialized:
            return

        else:
            type(self).initialized = True

        self.cfg = cfg
        self.param_dict = param_dict

        #Initialize functions
        for f in type(self).__bases__:
            if issubclass(f, IAdapterFunction):
                f.__init__(self, f.__name__)
    
    def get_cfg_template_path(self):
        raise NotImplementedError()

    def support_function(self, func_name, version):
        pass
