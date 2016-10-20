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

from xml.dom import minidom

class UnspecifyWorkspace(Exception):
    pass

class Config:
    '''
        A workspace file is a xml file. The format is like:
        <?xml version="1.0" encoding="utf-8"?><Workspace>
            <key name="k1">
                <val name="v1" value="aaa" />
                <val name="v2" value="aba" />
                <key name="k2">
                    <val name="v3" value="aca" />
                    <val name="v4" value="ada" />
                </key>
            </key>
        </Workspace>
    '''
    def __init__(self, path = None, parent = None, root = None, dom = None):
        '''
            Config() -> Config
            Config(path) -> Config

            Load or create a workspace. Don't use paren and root, they are
            used by te class itself.
        '''
        self.keys = {}
        self.values = {}
        self.path = None
        self.parent = None

        if path != None:
            #Load workspace
            self.path = path
            try:
                f = self.open(path, "r")

            except FileNotFoundError(e):
                print("Failed to open workspace \"%s\"."%(path))
                raise e

            self.dom = minidom.parse(f)
            f.close()
            self.root = self.dom.documentElement
            self.__load()

        if parent != None:
            self.parent = parent
            self.root = root
            self.dom = dom
            self.__load()

        else:
            self.dom = minidom.getDOMImplementation().createDocument(None,
                    "Workspace", None)
            self.root = self.dom.documentElement
            self.__load()

    def save(self, path = None):
        '''
            Save workspace.
        '''
        if path != None:
            self.path = path

        if self.parent != None:
            self.parent.save(path)

        else:
            f = open(self.path, "w")
            self.dom.writexml(self.file, addindent='',
                    newl='', encoding='utf-8')
            f.close()

    def __load(self):
        #Get keys
        key_nodes = self.root.getElementsByTagName("key")

        for kn in key_nodes:
            node_name = kn.getAttribute("name").encode('utf-8').decode()
            if node_name == "":
                raise UnspecifyWorkspace("The key requires a name.")

            self.keys[node_name] = Config(parent = self, root = kn, dom = self.dom)
            
        #Get values
        value_nodes = self.root.getElementsByTagName("val")
        for vn in value_nodes:
            value_name = vn.getAttribute("name").encode('utf-8').decode()
            if value_name == "":
                raise UnspecifyWorkspace("The value requires a name.")

            self.values[value_name] = vn

        return

    def add_key(self, path):
        '''
            cfg.add_key(path) -> Config

            Create new key.
        '''
        pass

    def get_key(self, path):
        '''
            cfg.get_key(path) -> Config
            
            Get child key.
        '''
        if path == "":
            return self

        try:
            if path[0] == '/':
                begin_key = self
                while begin_key.parent != None:
                    begin_key = begin_key.parent
                subpath = path.strip("/")
                return begin_key.get_key(subpath)

            elif path[0] == '.':
                name = path.split("/")[0]

                if name == "..":
                    begin_key = self.parent

                elif name == ".":
                    begin_key = self

                else:
                    raise KeyError(path)

                subpath = path[len(name) + 1 :].strip("/")
                return begin_key.get_key(subpath)

            else:
                begin_key = self
                name = path.split("/")[0]
                subpath = path[len(name) + 1 :].strip("/")
                key = begin_key.keys[name]
                return key.get_key(subpath)

        except KeyError:
            raise KeyError(path)

    def get_value(self, name):
        '''
            cfg.get_value(name) -> str

            Get value.
        '''

        return self.values[name]

    def set_value(self, name, value):
        '''
            Set/create/remove value, if value is None, the value will be removed.
        '''
        pass

    def remove(self):
        '''
            Remove current key.
        '''
        pass



