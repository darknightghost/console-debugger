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

class Frame:
    def __init__(self, parent, rect):
        self.parent = parent
        self.rect = rect
        self.alive = True

    def close(self):
        pass

    def resize(self, rect):
        pass

    def input(self, key,  mouse):
        pass

    def draw(self, pose, color, string):
        pass

    def update(self):
        pass

    def dispatch_msg(self, msg):
        pass

    def set_focus(self, stat):
        pass
