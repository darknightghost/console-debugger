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

from tui import *
from tui.window import *
from tui.controls import *
from plugins.PluginWnd import *

class SourceWnd(PluginWnd):
    def __init__(self, text, parent, rect, cfg, plugin, path):
        self.path = path
        PluginWnd.__init__(self, text, parent, rect, cfg, plugin)

    def init_window(self):
        self.regist_msg_func(Message.MSG_CHANGED, self.on_change)

        self.m_scoll_vertical = Scollbar("", self, Rect(Pos(0,
            self.rect.size.width - 1),
            Size(1, self.rect.size.height)),
            direction = Scollbar.VERTICAL)

        self.m_scoll_vertical.set_max_value(30)
        self.m_scoll_vertical.show()


    def on_change(self, msg):
        if msg.data == self.m_scoll_vertical:
            self.draw(Pos(0, 0), "%d"%(self.m_scoll_vertical.get_value()),
                    Color.get_color(Color.RED, Color.BLACK))
