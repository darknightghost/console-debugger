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
import importlib
import os
import log

def load_adapter(cfg, param_dict):
    name = None
    if not "a" in param_dict.keys():
        adaper_cfg = cfg.get_key("adapter")
        if not adaper_cfg.has_value("name"):
            print("Missing adapter.")
            return None

        else:
            name= adaper_cfg.get_value("name")

    else:
        name = param_dict["a"]

    if not name in get_adapter_list():
        print("Unknow adapter \"%s\"."%(name))
        return None

    adapter_module = importlib.import_module("adapters.%s.adapter"%(name))
    return adapter_module.Adapter(adaper_cfg, param_dict)

def get_adapter_list():
    adapter_dir = os.path.split(os.path.realpath(__file__))[0]
    files = os.listdir(adapter_dir)
    ret = []
    for t in files:
        if os.path.isdir(adapter_dir + "/" + t) and t != "__pycache__":
            ret.append(t)
    return ret

