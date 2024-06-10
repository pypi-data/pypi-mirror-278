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



from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Union

from mkdocs.config import config_options as C

from ..messages import Lang
from ..plugin.maestro_tools import CopyableConfig






@dataclass
class ArgConfig:

    name: str
    """ Argument name """

    py_type: Any
    """ Type used in the concrete python implementation """

    default: Optional[Any] = None
    """ Default value for the Config type. Ignored if None (use is_optional for this). """

    conf_type: Optional[Any] = None
    """
    ConfigOption related type. Created automatically from py_type if None, unless default
    is not None.
    """

    is_optional: bool = False
    """ If True, add a C.Optional wrapper around the conf_type """

    in_config: bool = True
    """ If False, this argument will not be added to the Config class/objects """

    docs: str = ""
    """ Text to use when building the "summary" args tables in the docs """

    docs_default_as_type: bool = True
    """ If True, use the default value instead of the type in the as_docs_table output. """

    deprecated_source: Optional[str] = None
    """
    Path attributes chaining of a deprecated config option: if this option is not None at
    runtime, the current option should be overridden with the one from the old option.
    """

    index: Optional[int] = None
    """
    Index of the argument in the *args tuple, if it's positional.
    If index is -1, means the argument itself represents a varargs argument.
    """

    path: str = ''
    """ MaestroBase property name (ConfigExtractor) """

    in_docs: bool = True
    """
    If False, this argument will not be present in the docs (tables of arguments, signatures).
    """

    docs_type: str = ""
    """ String replacement for the types in the docs """

    ide_link: bool=True

    transfer_processor: Optional[Callable[[Any],Any]] = None


    @property
    def is_positional(self):
        return self.index is not None


    def __post_init__(self):

        if self.in_config:

            if self.conf_type is None:
                # If default is None, it's equivalent to "no default", actually)
                self.conf_type = C.Type(self.py_type, default=self.default)

            if self.is_optional and self.default is None:
                self.conf_type = C.Optional(self.conf_type)

        if isinstance(self.deprecated_source,str):
            self.deprecated_source = tuple(self.deprecated_source.split('.'))


    def copy(self, **kw):
        args = {
            k: getattr(self,k) for k in self.__class__.__annotations__      # pylint: disable=no-member
        }
        args.update(kw)
        return self.__class__(**args)


    def get_type_str(self):
        if self.docs_default_as_type and self.default is not None:
            return repr(self.default)
        return self.py_type.__name__


    def get_docs_type(self):
        return self.docs_type or self.py_type.__name__


    def to_config(self):
        return self.conf_type

    def process_value_from_old_location(self, value):
        return value if not self.transfer_processor else self.transfer_processor(value)


    @property
    def doc_name_type_min_length(self):
        return 1 + len(self.name) + len(self.get_docs_type())


    def signature(self, size:int=None):
        length   = self.doc_name_type_min_length
        n_spaces = length if size is None else size - length + 1
        return f"\n    { self.name}:{ ' '*n_spaces }{ self.get_docs_type() } = {self.default!r},"


    def as_table_row(self, for_resume=False):

        if for_resume:
            a,b,doc = self.name, self.get_type_str(), self.docs
            if self.ide_link:
                doc += f"<br>_([plus d'informations](--IDE-{ self.name }))_"
        else:
            a,b,doc = f"#!py { self.get_docs_type() }", repr(self.default), self.docs

        return f"| `{ a }` | `#!py { b }` | { doc } |"










class MacroConfig:
    """
    Class making the link between:
        - The actual python implementation
        - The docs content (avoiding aou of synch docs)
        - The Config used for the .meta.pmt.yml features. Note that optional stuff "there" is
          different from an optionality (or it's absence) in the running macro/python layer.

    Those instances represent the config "starting point", so all defaults are applied here,
    for the Config implementation.
    When extracting meta files of meta headers, the CopyableConfig instances will receive dicts
    from the yaml content, and those will be merged in the current config, so the dict itself
    can contain only partial configs, it's not a problem. Hence, should be "C.Optional" _only_
    values that could be None at runtime as an actual/useful value.
    """

    def __init__(self, name, *args:ArgConfig, in_config=True,  in_docs=True):

        self.in_config: bool = in_config
        self.in_docs:   bool = in_docs
        self.name:      str = name
        self.args:      Dict[str,ArgConfig] = {arg.name: arg for arg in args}

        if len(self.args) != len(args):
            raise ValueError(name+": duplicate arguments names.\n"+str(args))

    def __getattr__(self, prop):
        if prop not in self.args:
            raise AttributeError(prop)
        return self.args[prop]


    def get_macro_arg_config(self, name) -> Union[None, 'MacroConfig']:
        return getattr(self, 'IDE' if name=='IDEv' else name, None)


    def args_with_path(self):
        """
        Extract all the ArgConfig instances with their path attribute in the plugin config.
        """

        def dfs(obj: Union[MacroConfig,ArgConfig] ):
            path.append(obj.name)
            if isinstance(obj, ArgConfig):
                yield obj, tuple(path)
            else:
                for child in obj.args.values():
                    yield from dfs(child)
            path.pop()

        path = []
        return dfs(self)


    def build_accessors(self):
        for arg,path in self.args_with_path():
            if arg.index == -1:
                continue
            arg.path = '_'.join(path)


    def to_config(self):
        """
        Convert recursively to the equivalent CopyableConfig object.
        """
        class_name = ''.join(map(str.title, self.name.split('_'))) + 'Config'
        extends = (CopyableConfig,)
        body = {
            name: arg.to_config()
                for name,arg in self.args.items()
                if arg.in_config
        }
        kls = type(class_name, extends, body)
        return C.SubConfig(kls)


    def as_docs_table(self):
        """
        Converts all arguments to a 3 columns table (data rows only!):  name + type + help.
        No indentation logic is added here.
        """
        return '\n'.join(
            arg.as_table_row(True) for arg in self.args.values() if arg.in_docs
        )

    def signature_for_docs(self):
        """
        Converts the MacroConfig to a python signature for the docs, ignoring arguments that
        are not "in_docs".
        """
        args = [arg for arg in self.args.values() if arg.in_docs]
        size = max( arg.doc_name_type_min_length for arg in args )
        lst  = [ arg.signature(size) for arg in args ]
        if args[0].name=='py_name':
            lst.insert(1, "\n    *,")

        return f"""
```python
{ '{{' } { self.name }({ ''.join(lst) }
) { '}}' }
```
"""








PY_GLOBAL = MacroConfig(
    '',
    ArgConfig(
        'py_name', str, default="", index=0,
        docs = "Chemin relatif vers le fichier `{exo}.py` et les éventuels fichiers annexes, sur "
               "lesquels baser l'IDE.",
    ),
    ArgConfig(
        'ID', int, in_config=False, docs_type="None|int",
        docs="À utiliser pour différencier deux IDEs utilisant les mêmes fichiers [{{annexes()}}]"
             "(--ide-files), afin de différencier leurs `id` (nota: $ID \\ge 0$)."
    ),
    ArgConfig(
        'SANS', str, default="",
        docs = "Pour interdire des fonctions builtins, des méthodes ou des modules : chaîne de "
               "noms séparés par des virgules et/ou espaces."
    ),
    ArgConfig(
        'WHITE', str, default="",
        docs = "(_\"White list\"_) Ensemble de noms de modules/packages à pré-importer avant que "
               "les interdictions ne soient mises en place (voir argument `SANS` ; `WHITE` _est "
               "normalement {{ orange('**obsolète**') }}_)."
    ),
    ArgConfig(
        'REC_LIMIT', int, default=-1,
        docs = "Pour imposer une profondeur de récursion maximale. Nota: ne jamais descendre en-"
               "dessous de 20."
    ),
)


MOST_LIKELY_USELESS_ID = PY_GLOBAL.ID.copy(
    docs="À utiliser pour différencier deux appels de macros différents, dans le cas où "
         "vous tomberiez sur une collision d'id (très improbable, car des hachages sont "
         "utilisés. Cet argument ne devrait normalement pas être nécessaire)."
)

def _py_globals_copy_gen(py_name_replacement:ArgConfig):
    return (
        MOST_LIKELY_USELESS_ID if name=='ID'
        else py_name_replacement if name=='py_name'
        else arg.copy()
        for name,arg in PY_GLOBAL.args.items()
    )




IDE = MacroConfig(
    'IDE',
    *PY_GLOBAL.args.values(),
    ArgConfig(
        'MAX', int, default=5, docs_type="int|'+'",
        deprecated_source = 'ides.max_attempts_before_corr_available',
        docs = "Nombre maximal d'essais de validation avant de rendre la correction et/ou les "
               "remarques disponibles."
    ),
    ArgConfig(
        'LOGS', bool, default=True,
        deprecated_source = 'ides.show_assertion_code_on_failed_test',
        docs = "{{ red('Durant des tests de validation') }}, si LOGS est `True`, le code "
               "complet d'une assertion est utilisé comme message d'erreur, quand "
               "l'assertion a été écrite sans message."
    ),
    ArgConfig(
        'MAX_SIZE', int, default=30,
        deprecated_source = 'ides.default_ide_height_lines',
        docs = "Impose la hauteur maximale possible pour un éditeur, en nombres de lignes."
    ),
    ArgConfig(
        'TERM_H', int, default=10,
        deprecated_source = 'ides.default_height_ide_term',
        docs = "Impose le nombre de lignes du terminal."
    ),
)






TERMINAL = MacroConfig(
    'terminal',
    *_py_globals_copy_gen( PY_GLOBAL.py_name.copy(
        docs = "Crée un terminal isolé utilisant le fichier python correspondant (sections "
               "autorisées: `env`, `env_term`, `post_term`, `post` et `ignore`)."
    )),
    ArgConfig(
        'TERM_H', int, default=10,
        deprecated_source = 'ides.default_height_isolated_term',
        docs = "Impose le nombre de lignes du terminal. [Voir ici](--IDE-TERM_H) pour les "
               "réglages globaux."
    ),
    ArgConfig(
        'FILL', str, default='', ide_link=False,
        docs = "Commande à afficher dans le terminal lors de sa création.<br>{{red('Uniquement "
               "pour les terminaux isolés.')}}"
    ),
)






PY_BTN = MacroConfig(
    'py_btn',
    *( arg.copy(in_docs = arg.name in ('py_name', 'ID'))
       for arg in _py_globals_copy_gen( PY_GLOBAL.py_name.copy(
            docs="Crée un bouton isolé utilisant le fichier python correspondant (uniquement "
                "`env` et `ignore`)."
    ))),
    ArgConfig(
        'WRAPPER', str, default='div', ide_link=False,
        docs = "Type de balise dans laquelle mettre le bouton."
    ),
    ArgConfig(
        'HEIGHT', int, is_optional=True, ide_link=False,
        docs = "Hauteur par défaut du bouton."
    ),
    ArgConfig(
        'WIDTH', int, is_optional=True, ide_link=False,
        docs = "Largeur par défaut du bouton."
    ),
    ArgConfig(
        'SIZE', int, is_optional=True, ide_link=False,
        docs = "Si défini, utilisé pour la largeur __et__ la hauteur du bouton."
    ),
    ArgConfig(
        'ICON', str, default="", ide_link=False,
        docs = "Par défaut, le bouton \"play\" des tests publics des IDE est utilisé."
               "<br>Peut également être une icône `mkdocs-material`, une adresse vers une image "
               "(lien ou fichier), ou du code html.<br>Si un fichier est utiliser, l'adresse doit "
               "être relative au `docs_dir` du site construit."
    ),
    ArgConfig(
        'TIP', str, default=Lang.py_btn.msg, ide_link=False,
        docs = "Message à utiliser pour l'info-bulle."
    ),
    ArgConfig(
        'TIP_SHIFT', int, default=50, ide_link=False,
        docs = "Décalage horizontal de l'info-bulle par rapport au bouton, en `%` (50% correspond "
        "à un centrage)."
    ),
    ArgConfig(
        'TIP_WIDTH', float, default=0.0, ide_link=False,
        docs = "Largeur de l'info-bulle, en `em` (`#!py 0` correspond à une largeur automatique)."
    ),
)






SECTION = MacroConfig(
    'section',

    # Required on the python side, but should never be given through "meta", so it has to be
    # non blocking on the config side:
    PY_GLOBAL.py_name.copy(
        docs="[Fichier python {{ annexe() }}](--ide-files).", ide_link=False,
    ),
    ArgConfig(
        'section', str, index=1, is_optional=True, ide_link=False,
        docs = "Nom de la section à extraire."
    ),
)






PY = MacroConfig(
    'py',

    # Required on the python side, but should never be given through "meta", so it has to be
    # non blocking on the config side:
    ArgConfig(
        'py_name', str, is_optional=True, index=0, ide_link=False,
        docs = "Fichier source à utiliser (sans l'extension)."
    ),
)






MULTI_QCM = MacroConfig(
    'multi_qcm',

    # Required on the python side, but should never be given through "meta": must not be blocking:
    ArgConfig(
        '*inputs', list, index=-1, in_config=False, docs_default_as_type=False, ide_link=False,
        docs = "Chaque argument individuel est une liste décrivant une question avec ses choix "
               "et réponses."
    ),
    ArgConfig(
        'hide', bool, default=False, ide_link=False,
        docs = "Si `#!py True`, un masque apparaît au-dessus des boutons pour signaler à "
               "l'utilisateur que les réponses resteront cachées après validation."
    ),
    ArgConfig(
        'multi', bool, default=False, ide_link=False,
        docs = "Réglage pour toutes les questions du qcms, indiquant si les questions n'ayant "
               "qu'une seule bonne réponse sont à choix multiples ou pas."
    ),
    ArgConfig(
        'shuffle', bool, default=False, ide_link=False,
        docs = "Mélange les question et leurs choix ou pas."
    ),
    ArgConfig(
        'admo_kind', str, default="!!!", ide_link=False,
        docs = "Type d'admonition dans laquelle les questions seront rassemblées (`'???'` et "
               "`'???+'` dont également utilisables, pour des qcms repliés ou \"dépliés\")."
    ),
    ArgConfig(
        'admo_class', str, default="tip", ide_link=False,
        docs = "Pour changer la classe d'admonition ou en rajouter d'autres si besoin."
               "<br>Il est également possible d'ajouter d'autres classes si besoin, en "
               "les séparant par des espaces (ex: `#!py 'warning custom-class'`)."
    ),
    ArgConfig(
        'qcm_title', str, default=Lang.qcm_title.msg, ide_link=False,
        docs = "Pour Changer le titre apparaissant dans l'admonition."
    ),
    ArgConfig(
        'DEBUG', bool, default=False, ide_link=False,
        docs = "Affiche ou non dans la console le code markdown généré pour ce qcm durant le build."
    ),
)





ARGS_MACRO_CONFIG = MacroConfig(
    'args', IDE, TERMINAL, PY_BTN, SECTION, MULTI_QCM, PY
)


ARGS_MACRO_CONFIG.build_accessors()
