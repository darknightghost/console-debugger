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
                f = open(path, "r")

            except FileNotFoundError as e:
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

    def add_key(self, name):
        '''
            cfg.add_key(name) -> Config

            Create new key.
        '''
        def check_name(name):
            if name == "":
                return False

            for c in name:
                if not ((ord(c) >= ord("A") and ord(c) <= ord("Z")) \
                        or (ord(c) >= ord("a") and ord(c) <= ord("z")) \
                        or (ord(c) >= ord("0") and ord(c) <= ord("9")) \
                        or (c == '_')):
                    return False

            return True

        if not check_name(name):
            raise NameError("Name \"%s\" is illegae."%(name))

        elif name in self.keys.keys():
            raise NameError("Key \"%s\" already exists."%(name))

        new_key = self.dom.createElement("key")
        new_key.setAttribute("name", name)
        self.appendChild(new_key)

        return new_key

    def add_key_by_path(self, path):
        '''
            cfg.add_key_by_path(path) -> Config

            Create new key, parent keys will be created automatically.
        '''
        if path[-1] == '/':
            path = path[: -1]

        name = path.split("/")[-1]
        subpath = path[: -len(name)]
        try:
            self.get_key(subpath)

        except KeyError:
            self.add_key_by_path(subpath)

        return self.add_key(name)

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
        val_node = self.values[name]
        return val_node.getAttribute("value")

    def set_value(self, name, value):
        '''
            Set/create/remove value, if value is None, the value will be removed.
        '''
        def check_name(name):
            if name == "":
                return False

            for c in name:
                if not ((ord(c) >= ord("A") and ord(c) <= ord("Z")) \
                        or (ord(c) >= ord("a") and ord(c) <= ord("z")) \
                        or (ord(c) >= ord("0") and ord(c) <= ord("9")) \
                        or (c == '_')):
                    return False

            return True


        try:
            val_node = self.values[name]

        except KeyError:
            if value != None:
                #Create value
                if not check_name(name):
                    raise NameError("Illegal value name : \"%s\"."%(name))

                new_val = self.dom.createElement("val")
                new_val.setAttribute("name", name)
                new_val.setAttribute("value", value)

        else:
            if value == None:
                #Remove value
                if name in self.values.keys():
                    val_node = self.values[name]
                    self.root.removeChild(val_node)
                    self.value.pop(name)

            else:
                #Set value
                val_node = self.values[name]
                val_node.setAttribute("value", value)

    def remove(self):
        '''
            Remove current key.
        '''
        if self.parent != None:
            self.parent.root.removeChild(self.root)
            self.parent.keys.pop(self.root.getAttribute("name"))

        return



