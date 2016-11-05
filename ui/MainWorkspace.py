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
import os

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

        self.plugin_mgr = plugins.PluginManager(adapter, 
                self.cfg.get_key("/plugins"), self)

        #Regist commands
        #Close workspace
        self.reg_command("qa", self.on_cmd_qa, None)
        #Split workspace
        self.reg_command("sp", self.on_cmd_sp, None)
        #Vertical split wprkspace
        self.reg_command("vs", self.on_cmd_vs, None)
        #Close tab
        self.reg_command("q", self.on_cmd_q, None)
        #Close view
        self.reg_command("qv", self.on_cmd_qv, None)
        #Prev tag
        self.reg_command("pt", self.on_cmd_pt, None)
        #Next tag
        self.reg_command("nt", self.on_cmd_nt, None)
        #Show help
        self.reg_command("help", self.on_cmd_help, None)
        #Save workspace
        self.reg_command("w", self.on_cmd_w, self.complete_path)
        #Save workspace and quit
        self.reg_command("wqa", self.on_cmd_wqa, self.complete_path)

    def on_cmd_qa(self, command):
        #Quit
        self.close()

    def on_cmd_sp(self, command):
        #Split tab view
        self.focused_view.split(TagsView.SP_HORIZONTAL)

    def on_cmd_vs(self, command):
        #Vertical split the tab view
        self.focused_view.split(TagsView.SP_VERTICAL)

    def on_cmd_q(self, command):
        #Close tab
        if self.focused_view != None:
            if self.focused_view.focused_child != None:
                self.focused_view.focused_child.close()

            else:
                self.focused_view.close()
                if len(self.views) > 0:
                    self.views[0].set_focus(True)

    def on_cmd_qv(self, command):
        #Close view
        if self.focused_view != None:
            self.focused_view.close()
            if len(self.views) > 0:
                self.views[0].set_focus(True)

            else:
                self.focused_view = None

    def on_cmd_pt(self, command):
        #Previous tab
        self.focused_view.prev_tag()

    def on_cmd_nt(self, command):
        #Next tab
        self.focused_view.next_tag()

    def on_cmd_help(self, command):
        #Show help
        pass

    def on_cmd_w(self, command):
        #Save workspace
        try:
            if len(command) > 1:
                self.cfg.save(command[1])

            else:
                self.cfg.save()

        except IOError:
            return "Requires path to save."

    def on_cmd_wqa(self, command):
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

    def complete_path(self, compstr):
        if compstr == "":
            return []

        compath = ""
        compname = ""
        if compstr[-1] == os.path.sep:
            compath = compstr

        else:
            compath = compstr[: compstr.rfind(os.path.sep) + 1]
            compname = compstr[compstr.rfind(os.path.sep) + 1 :]

        try:
            dir_list = os.listdir(compath)

        except Exception:
            return []

        ret = []
        for n in dir_list:
            if n[: len(compname)] == compname:
                ret.append(compath + n)

        return ret

    def on_create(self):
        #Load config
        self.__load()

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
