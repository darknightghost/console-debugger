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

from config import config

class IAdapterFunction:
    def __init__(self, func_name):
        #Get config
        try:
            self.__dict__["%s_cfg"] = self.cfg.get_key("functions/%s"%(func_name))

        except config.ConfigKeyError:
            self.__dict__["%s_cfg"] = self.cfg.add_key_by_path("functions/%s"%(func_name))

        #Initialize function
        try:
            self.__dict__["%s_init"](self)

        except KeyError:
            raise NotImplementedError("Initialization function of \"%s\" does not exists."%(func_name))

