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
from ui.CDBGTagsView import *
import plugins
import log

class MainWorkspace(Workspace):
    def __init__(self, adapter, params, cfg):
        self.adapter = adapter
        Workspace.__init__(self)
        self.cfg = cfg
        self.view_cfg = cfg.get_key("views")
        try:
            self.views_key = self.view_cfg.get_key("views")

        except KeyError:
            self.views_key = self.view_cfg.add_key("views")

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
            try:
                if len(command) > 1:
                    self.cfg.save(command[1])

                else:
                    self.cfg.save()

            except IOError:
                return "Requires path to save."

        elif command[0] == "wq":
            #Save workspace and quit
            try:
                if len(command) > 1:
                    self.cfg.save(command[1])

                else:
                    self.cfg.save()

                self.close()
                return

            except IOError:
                return "Requires path to save."

        else:
            return plugins.dispatch_plugin_cmd(command)

    def on_create(self):
        #Load config
        self.__load()

    def on_shotcut_key(self, key):
        return plugins.dispatch_shotcut_key(key)

    def __load(self):
        self.size = Size(int(self.view_cfg.get_value("width")),
                int(self.view_cfg.get_value("height")))
        self.client_size = Size(self.size.width, self.size.height - 1)
        for i in range(1, len(self.views_key.list_keys())):
            try:
                v_key = self.views_key.get_key(str(i))
                CDBGTagsView(self, Rect(Pos(0, 0), 
                    Size(self.client_size.width, self.client_size.height)),
                    v_key)

            except KeyError:
                raise UnspecifyWorkspace()

        wnd_size = self.stdscr.getmaxyx()
        self.resize(Size(wnd_size[1], wnd_size[0]))

    def resize(self, size):
        Workspace.resize(self, size)
        self.view_cfg.set_value("width", str(size.width))
        self.view_cfg.set_value("height", str(size.height))

    def create_init_view(self):
        try:
            v0_key = self.views_key.get_key("0")

        except KeyError:
            v0_key = self.views_key.add_key("0")

        return CDBGTagsView(self, Rect(Pos(0, 0), 
            Size(self.client_size.width, self.client_size.height)), v0_key)
