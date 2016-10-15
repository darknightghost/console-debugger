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
from tui.window import *

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

        elif command == "qw":
            if self.focused_view != None:
                if self.focused_view.focused_child != None:
                    self.focused_view.focused_child.close()

        elif command == "qv":
            if self.focused_view != None:
                self.focused_view.close()
                if len(self.views) > 0:
                    self.views[0].set_focus(True)

                else:
                    self.focused_view = None

        else:
            return "Unknow command."

    def on_create(self):
        wnd = Window("aaa", self.focused_view, Rect(Pos(1,1),Size(
            self.focused_view.client_size.width,
            self.focused_view.client_size.height)))
        wnd.set_focus(True)
        wnd.show()

        for i in range(0, 8):
            wnd = Window(chr(ord("b") + i) * 3, self.focused_view, Rect(Pos(1,1),Size(
                self.focused_view.client_size.width,
                self.focused_view.client_size.height)))

        #Load config
        #Load plugins
        pass

    def on_shotcut_key(self, key):
        pass
