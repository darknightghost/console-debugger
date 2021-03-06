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

import tui
from tui.tagsview import *
from config import config
import plugins

class CDBGTagsView(TagsView):
    def __init__(self, parent, rect, cfg):
        self.cfg = cfg
        try:
            top = int(cfg.get_value("top"))
            left = int(cfg.get_value("left"))
            width = int(cfg.get_value("width"))
            height = int(cfg.get_value("height"))
            TagsView.__init__(self, parent, Rect(Pos(top, left),
                Size(width, height)))
            self.__load()

        except config.ConfigValueError:
            cfg.set_value("top", str(rect.pos.top))
            cfg.set_value("left", str(rect.pos.left))
            cfg.set_value("width", str(rect.size.width))
            cfg.set_value("height", str(rect.size.height))
            TagsView.__init__(self, parent, rect)

    def create(self, rect):
        new_cfg = self.cfg.add_key_by_path("/views/views/%d"%(len(self.parent.views)))
        return CDBGTagsView(self.parent, rect, new_cfg)

    def __load(self):
        #Load docking relationships
        #Top
        try:
            top_docks = self.cfg.get_value("top_docked")
            if top_docks != "":
                for i in top_docks.split(","):
                    try:
                        i = int(i)
                        v = self.parent.views[i]
                        if v not in self.top_docked:
                            self.top_docked.append(v)

                        if self not in v.bottom_docked:
                            v.bottom_docked.append(self)

                    except IndexError:
                        continue

        except Exception:
            pass

        #Bottom
        try:
            bottom_docks = self.cfg.get_value("bottom_docked")
            if bottom_docks != "":
                for i in bottom_docks.split(","):
                    try:
                        i = int(i)
                        v = self.parent.views[i]
                        if v not in self.bottom_docked:
                            self.bottom_docked.append(v)

                        if self not in v.top_docked:
                            v.top_docked.append(self)

                    except IndexError:
                        continue

        except Exception:
            pass

        #Left
        try:
            left_docks = self.cfg.get_value("left_docked")
            for i in left_docks.split(","):
                try:
                    i = int(i)
                    v = self.parent.views[i]
                    if self.parent.views[i] not in self.left_docked:
                        self.left_docked.append(v)

                    if self not in v.right_docked:
                        v.right_docked.append(self)

                except IndexError:
                    continue

        except Exception:
            pass

        #Right
        try:
            right_docks = self.cfg.get_value("right_docked")
            for i in right_docks.split(","):
                try:
                    i = int(i)
                    v = self.parent.views[i]
                    if v not in self.right_docked:
                        self.right_docked.append(v)

                    if self not in v.left_docked:
                        v.left_docked.append(self)

                except IndexError:
                    continue

        except Exception:
            pass

        #Focus
        try:
            if self.cfg.get_value("focused") == "True":
                self.set_focus(True)

        except config.ConfigValueError:
            pass

        #Load windows
        try:
            windows_cfg = self.cfg.get_key("windows")

        except config.ConfigKeyError:
            windows_cfg = self.cfg.add_key("windows")

        #Open windows
        for k in windows_cfg.keys:
            wnd_key = windows.get_key(k)
            plugin = self.parent.plugin_mgr.get_plugin(wnd_key.get_value("plugin"))
            if wnd_key.get_value("type") == "plugin":
                argv = list(tui.Command(wnd_key.get_value("argv")))
                plugin.open(wnd_key, self, argv)

            else:
                plugin.configure(wnd_key, self)

        try:
            focused_index = windows_cfg.get_value("focused")
            self.children[int(focused_index)].set_focus(True)

        except config.ConfigValueError:
            pass

    def open_plugin(self, plugin_name, argv):
        plugin = self.parent.plugin_mgr.get_plugin(plugin_name)

        if not plugin.openable():
            raise plugins.PluginNotFoundError(plugin_name)

        #Create config node
        windows_cfg = self.cfg.get_key("windows")
        cfg_node = windows_cfg.add_key(str(len(self.children)))
        cfg_node.set_value("plugin", plugin_name)
        cfg_node.set_value("type", "plugin")
        cfg_node.set_value("argv", str(tui.Command(argv)))
        try:
            result = plugin.open(cfg_node, self, argv)
            if not result:
                cfg_node.remove()

        except Exception as e:
            cfg_node.remove()
            raise e

    def configure_plugin(self, plugin_name):
        plugin = self.parent.plugin_mgr.get_plugin(plugin_name)

        if not plugin.configureable():
            raise plugins.PluginNotFoundError(plugin_name)

        #Create config node
        windows_cfg = self.cfg.get_key("windows")
        cfg_node = windows_cfg.add_key(str(len(self.children)))
        cfg_node.set_value("plugin", plugin_name)
        cfg_node.set_value("type", "configure")

        result = plugin.configure(cfg_node, self)
        if not result:
            cfg_node.remove()

    def on_resize(self, msg):
        self.cfg.set_value("top", str(self.rect.pos.top))
        self.cfg.set_value("left", str(self.rect.pos.left))
        self.cfg.set_value("width", str(self.rect.size.width))
        self.cfg.set_value("height", str(self.rect.size.height))
        TagsView.on_resize(self, msg)

    def on_get_focus(self, msg):
        self.cfg.set_value("focused", "True")
        TagsView.on_get_focus(self, msg)

    def on_lost_focus(self, msg):
        self.cfg.set_value("focused", "False")
        TagsView.on_lost_focus(self, msg)

    def save_docks(self):
        #Top
        top_str = ""
        for v in self.top_docked:
            try:
                top_str += str(self.parent.views.index(v)) + ","
            except ValueError:
                pass

        top_str = top_str.strip(",")
        self.cfg.set_value("top_docked", top_str)

        #Bottom
        bottom_str = ""
        for v in self.bottom_docked:
            try:
                bottom_str += str(self.parent.views.index(v)) + ","
            except ValueError:
                pass

        bottom_str = bottom_str.strip(",")
        self.cfg.set_value("bottom_docked", bottom_str)

        #Left
        left_str = ""
        for v in self.left_docked:
            try:
                left_str += str(self.parent.views.index(v)) + ","
            except ValueError:
                pass

        left_str = left_str.strip(",")
        self.cfg.set_value("left_docked", left_str)

        #Right
        right_str = ""
        for v in self.right_docked:
            try:
                right_str += str(self.parent.views.index(v)) + ","
            except ValueError:
                pass

        right_str = right_str.strip(",")
        self.cfg.set_value("right_docked", right_str)


    def split(self, direct):
        TagsView.split(self, direct)
        for v in self.parent.views:
            v.save_docks()

    def close(self):
        TagsView.close(self)

        self.cfg.remove()
        if self.parent.alive:
            for v in self.parent.views:
                v.cfg.rename("new_" + str(self.parent.views.index(v)))

            for v in self.parent.views:
                v.cfg.rename(str(self.parent.views.index(v)))

            for v in self.parent.views:
                v.save_docks()

    def remove_child(self, child):
        windows_cfg = self.cfg.get_key("windows")
        windows_cfg.get_key(str(self.children.index(child))).remove()
        TagsView.remove_child(self, child)
        for i in range(0, len(self.children)):
            self.children[i].cfg.rename(str(i))

        if self.focused_child == None:
            windows_cfg.set_value("focused", None)

        else:
            windows_cfg.set_value("focused", \
                    str(self.children.index(self.focused_child)))
