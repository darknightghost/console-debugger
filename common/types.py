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
import inspect

def check_arg_type(**arg_types):
    '''
        @check_arg_type(arg1 = (type1, type2, ...), arg2 = (type1, type2, ...), ...)

        Check argument types of function.
    '''
    def _deco(func):
        def _deco(*args, **kwargs):
            #Check arguments types
            arg_dict = inspect.getcallargs(func, *args, **kwargs)

            for name in arg_dict.keys():
                try:
                    type_correct = False
                    for t in arg_types[name]:
                        if isinstance(arg_dict[name], arg_types[name]):
                            type_correct = True

                    if not type_correct:
                        types = ""
                        for t in arg_types[name]:
                            if types != "":
                                types += ','

                            types += t.__name__

                        types = "(" + types + ")"

                        raise TypeError("Argument \"%s\" must be a instance of one of types in \"%s\" in function \"%s\"."\
                                %(name, types, func.__name__))

                except KeyError:
                    pass

            #Call function
            ret = func(*args, **kwargs)
            return ret

        return _deco

    return _deco

