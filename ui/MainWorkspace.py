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
    def __init__(self, adapter, params, cfg):
        self.adapter = adapter
        Workspace.__init__(self)
        self.cfg = cfg

    def on_command(self, command):
        if command[0] == "q":
            #Quit
            self.close()

        elif command[0] == "sp":
            #Split tab view
            self.focused_view.split(TagsView.SP_HORIZONTAL)

        elif command[0] == "vs":
            #Vertical split the tab view
            self.focused_view.split(TagsView.SP_VERTICAL)

        elif command[0] == "qt":
            #Close tab
            if self.focused_view != None:
                if self.focused_view.focused_child != None:
                    self.focused_view.focused_child.close()

        elif command[0] == "qv":
            #Close view
            if self.focused_view != None:
                self.focused_view.close()
                if len(self.views) > 0:
                    self.views[0].set_focus(True)

                else:
                    self.focused_view = None

        elif command[0] == "pt":
            #Previous tab
            self.focused_view.prev_tag()

        elif command[0] == "nt":
            #Next tab
            self.focused_view.next_tag()

        elif command[0] == "help":
            #Show help
            pass

        elif command[0] == "w":
            #Save workspace
            pass

        else:
            return "Unknow command."

    def on_create(self):
        #Load config
        #Load plugins
        pass

    def on_shotcut_key(self, key):
        pass
