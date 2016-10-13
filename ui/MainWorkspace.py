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

from tui.workspace import *
from tui.tagsview import *

class MainWorkspace(Workspace):
    def __init__(self, adapter, params):
        self.adapter = adapter
        Workspace.__init__(self)

    def on_command(self, command):
        if command == "q":
            self.close()
            return

        elif command == "sp":
            self.focused_view.split(TagsView.SP_HORIZONTAL)
            return

        elif command == "vs":
            self.focused_view.split(TagsView.SP_VERTICAL)
            return

        elif command == "sz":
            return str(self.size)
        elif command == "wn":
            return str(len(self.views))

        else:
            return "Unknow command."

    def on_create(self):
        pass

    def on_shotcut_key(self, key):
        pass
