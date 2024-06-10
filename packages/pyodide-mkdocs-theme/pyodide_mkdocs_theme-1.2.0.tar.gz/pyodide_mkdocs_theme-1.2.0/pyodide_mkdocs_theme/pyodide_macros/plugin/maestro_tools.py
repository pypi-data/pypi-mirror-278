"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""


import re
from typing import Any, TYPE_CHECKING
from argparse import Namespace

from mkdocs.config.base import Config
from mkdocs.config import config_options as C

from ..parsing import camel

if TYPE_CHECKING:
    from .pyodide_macros_plugin import PyodideMacrosPlugin







class CopyableConfig(Config):
    """
    CopyableConfig instances can copy themselves, merging them with a given dict-like object
    (potentially another mkdocs Config object) and return a brand new object.
    """

    def copy(self):
        """ Recursively create a copy of self """
        other = self.__class__()
        for k,v in self.items():
            other[k] = v.copy() if isinstance(v, CopyableConfig) else v
        return other



    def copy_with(self, yml_nested_dct:dict, consume_dict=False):
        """
        Create a "copy" of self, overriding any of its property with the matching content of
        the @yml_nested_dct argument.
        The original object is used as "tree hierarchy source", so anything in the dict object
        that doesn't already exist in the source structure will be ignored.

        @consume_dict: If True, the dict object to merge will be recursively mutated, removing
                       the data from it as they are used. This allows to know if something has
                       not been used from the @yml_nested_dct if some kind of validation of its
                       content is needed.

        NOTE: Identical sub configs are actually shared between the source object and the "copy".
              Only the updated branches use brand new objects.
        """
        def merge_dfs(new_config, yml_nested_dct:dict):
            for k in [*yml_nested_dct]:
                obj = getattr(new_config, k, None)
                if obj is None:
                    continue

                v = yml_nested_dct.pop(k) if consume_dict else yml_nested_dct[k]
                if isinstance(obj, CopyableConfig):
                    merge_dfs(obj, v)
                else:
                    new_config[k] = v

            return new_config

        return merge_dfs(self.copy(), yml_nested_dct)







class DeprecatedMsg(Namespace):

    moved = "this option is deprecated. It's equivalent is now: {}."

    removed = "This option is deprecated: it has no use anymore abd will be removed in the future."

    unsupported_macro = (
        "Macros using {} may not work anymore and will be removed in the future. Please contact "
        "the author of the theme if you need this macro/tool."
    )



def deprecated_option(prop:str, typ:Any, template:str, *extras_format:str):
    if not isinstance(typ, (C.Optional, C.Type)):
        typ = C.Optional(C.Type(typ))
    return C.Deprecated(message=template.format(prop, *extras_format), option_type=typ)




class ConfigExtractor:
    """
    Data descriptor extracting automatically the matching property name from the mkdocs config.
    An additional path (dot separated keys/properties) can be provided, that will be prepended
    to the property name.
    """

    def __init__(self, path='', *, prop=None, root='config'):
        self.prop = prop
        self.data = path,root
        self._getter = lambda _: None

    def __set_name__(self, _kls, over_prop):
        path,root = self.data
        if not self.prop: self.prop = over_prop

        # Using an evaluated function gives perfs equivalent to the previous version using a
        # cache, while keeping everything fully dynamic (=> prepare the way for meta.pmt.yml)
        props = 'obj.' + '.'.join((root, path, self.prop)).strip('.').replace('..','.')
        if not re.fullmatch(r'\w([\w.]*\w)?', props):
            raise ValueError("Invalid code:\n" + props)
        self._getter = eval("lambda obj: " + props)         # pylint: disable=eval-used

    def __get__(self, obj:'PyodideMacrosPlugin', kls=None):
        return self._getter(obj)

    def __set__(self, *a, **kw):
        raise ValueError(f"The {self.prop} property should never be reassigned")






class AutoCounter:
    """
    Counter with automatic increment. The internal value can be updated/rested by assignment.
    @warn: if True, the user will see a notification in the console about that counter being
    unmaintained so far (displayed once only).
    """

    def __init__(self, warn=False):
        self.cnt = 0
        self.warn_once = warn

    def __set_name__(self, _, prop:str):
        self.prop = prop        # pylint: disable=attribute-defined-outside-init

    def __set__(self, _:'PyodideMacrosPlugin', value:int):
        self.cnt = value

    def __get__(self, obj:'PyodideMacrosPlugin', __=None):
        if self.warn_once:
            self.warn_once = False
            obj.warn_unmaintained(f'The property {self.prop!r}')
        self.cnt += 1
        return self.cnt






def dump_and_dumper(props, obj, converter):

    if obj is None:
        class DumpNull:
            def __getattr__(self,_):
                return None
        obj = DumpNull()

    return { camel(prop): converter(getattr(obj, prop)) for prop in props }
