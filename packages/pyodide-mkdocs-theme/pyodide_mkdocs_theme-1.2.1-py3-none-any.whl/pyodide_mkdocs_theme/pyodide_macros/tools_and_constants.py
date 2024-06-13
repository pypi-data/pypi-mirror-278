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

# pylint: disable=too-few-public-methods, missing-module-docstring

from argparse import Namespace
from pathlib import Path
import re




class AutoDescriptor:
    """ StrEnum-like property for py3.11-
        If the item string doesn't match the name anymore, one can set the wanted name
        through the constructor, without changing the property name (but F2 will most
        likely also do the trick... Unless string version is actually used somewhere...)
    """

    def __init__(self, prop:str=None):      # allow to override the property name,
        self._prop = prop

    def __set_name__(self, _, prop:str):
        self._prop = self._prop or prop

    def __get__(self, _, __):
        return self._prop






# --------------------------------------------------------------------
# Various types aliasing, to disambiguate some arguments or constants
# --------------------------------------------------------------------



MACROS_WITH_INDENT = "py multi_qcm section IDEv?"
""" Regex patterns (fullmatch) identifying macros that are inserting multiline contents """

ICONS_IN_TEMPLATES_DIR = Path("assets/images")
""" Relative location of the icons/pictures for the buttons, in the templates directory """

PY_LIBS = 'py_libs' # If you change this, don't forget to update config.build.python_libs default
""" Default name for python libraries """

LZW_DELIMITER = "\x1e"    # Unambiguous separator
""" Separator used to structure de compressed strings, with custom LZW alogrithm """



PageUrl = str
""" Page url, as obtained through page.url """

EditorName = str
""" String reference in the form `editor_xxx` """






class IdeConstants(Namespace):
    """
    Global configuration and data for Ide related elements.
    """

    min_ide_id_digits: int = 8
    """ Id numbers (before hashing) will be 0 right padded """

    infinity_symbol: str = "∞"

    ide_buttons_path_template: str = str(
        "{lvl_up}" / ICONS_IN_TEMPLATES_DIR / "icons8-{button_name}-64.png"
    )
    """
    Template to reach the buttons png files from the current IDE.
    Template variables:   lvl_up, button_name
    """

    encryption_token: str = "ENCRYPTION_TOKEN"
    """
    Denote the start and end point of the content of the div tag holding correction and/or remark.
    (only used in the python layer: it is either removed in the on_page_context hook, or it's just
    not inserted at all if the encrypt_corrections_and_rems is False)
    """

    min_recursion_limit: int = 20
    """ Minimum recursion depth allowed. """

    hdr_pattern: re.Pattern = re.compile(r"#\s*-+\s*(?:HDR|ENV)\s*-+\s*#", flags=re.IGNORECASE)
    """ Old fashion way of defining the `env` code in the python source file (still supported). """








class Prefix:
    """ Enum like, holding the prefixes used to build html classes or ids in the project """

    editor_  = AutoDescriptor()
    """ To build the editor name id """

    global_ = AutoDescriptor()
    """ Extra prefix to build the id of the div holding the complete IDE thing """

    comment_ = AutoDescriptor()
    """ Extra prefix for the "toggle assertions button" """

    term_ = AutoDescriptor()
    """ Extra prefix for ids of IDE terminals """

    solution_ = AutoDescriptor()
    """ Extra prefix for the div holding the correction + REM """

    input_ = AutoDescriptor()
    """ Extra prefix for the hidden input (type=file) managing the code upload part """

    compteur_ = AutoDescriptor()
    """ Extra id prefix for the span holding the counter of an IDE """

    term_only_ = AutoDescriptor()
    """ Prefix for the id of a div holding an isolated terminal """

    btn_only_ = AutoDescriptor()
    """ Prefix for the id of an isolated 'ide button" """

    solo_term_ = AutoDescriptor()
    """ [OUTDATED] Prefix for the id of the fak div associated to an isolated terminal """

    py_mk_pin_scroll_input = AutoDescriptor()     # Used in the JS part only
    """ Id input, used to mark the current the view port top value when pyodide got ready """

    py_mk_qcm_id_ = AutoDescriptor()
    """ This is actually a CLASS prefix (because it's not possible to register an html id
        on admonitions)
    """







class HtmlClass:
    """ Enum like, holding html classes used here and there in the project. """

    py_mk_py_btn = AutoDescriptor()
    """ Wrapper (div, but not only!) around isolated PyBtn elements """

    py_mk_hidden = AutoDescriptor()    # Was "py_mk_hide"
    """ Things that will have display:none """

    py_mk_ide = AutoDescriptor()       # But "py_mk_ide"... Lost 3 hours because of that 'h'...
    """ Identify div tags holding IDEs """

    terminal = AutoDescriptor()
    """ Identify jQuery terminals. Note: also used by them => do not change it """

    py_mk_terminal_solo = AutoDescriptor()
    """ Identify the divs that will hold isolated jQuery terminals, once they are initialized """

    py_mk_terminal_ide = AutoDescriptor()
    """ Identify divs that hold jQuery terminals under an editor, once they are initialized """

    rem_fake_h3 = AutoDescriptor()
    """ To make the "Remarques:" span in the solution admonitions look like a h3 """

    term_editor = AutoDescriptor()
    """ Prefix for the class mode of a terminal (horizontal or vertical) """

    py_mk_terminal = AutoDescriptor()
    """ Generic class for pyodide terminals (put on the div holding the jQuery terminal) """

    py_mk_wrapper = AutoDescriptor()
    """ Prefix for the class mode of the div holding an IDE """

    ide_separator = AutoDescriptor()
    """ might be used with the _v suffix """

    skip_light_box = AutoDescriptor()
    """ Img tab with this class won't be touched by glightbox """

    comment = AutoDescriptor()

    tooltip = AutoDescriptor()

    compteur = AutoDescriptor()

    compteur_wrapper = AutoDescriptor()

    compteur_txt = AutoDescriptor()

    ide_buttons_div = AutoDescriptor()

    ide_buttons_div_wrapper = AutoDescriptor()

    stdout_ctrl = AutoDescriptor("stdout-ctrl")

    stdout_wrap_btn = AutoDescriptor("stdout-wraps-btn")

    term_wrapper = AutoDescriptor()
    """ Prefix for the div holding a terminal and its buttons """

    term_btns_wrapper = AutoDescriptor()
    """ Prefix for the div holding a terminal and its buttons """




    py_mk_admonition_qcm = AutoDescriptor()
    """ Admonition containing a QCM """

    qcm_shuffle = AutoDescriptor()
    """ The questions and items must be shuffled if present """

    qcm_hidden = AutoDescriptor()
    """ The answers will be revealed if present """

    qcm_multi = AutoDescriptor()
    """ The user can select several answers """

    qcm_single = AutoDescriptor()
    """ The user can select only one answer """









class SiblingFile(Namespace):
    """ Suffixes to use to get the names of the different files related to one problem """
    exo = '.py'
    test = '_test.py'
    corr = '_corr.py'
    rem = '_REM.md'
    vis_rem = '_VIS_REM.md'




class ScriptSection:
    """ Name of each possible section used in a "monolithic" python file """
    ignore  = AutoDescriptor()

    env = AutoDescriptor()
    env_term = AutoDescriptor()
    user = AutoDescriptor("code")
    corr = AutoDescriptor()
    tests = AutoDescriptor()
    secrets = AutoDescriptor()
    post_term = AutoDescriptor()
    post = AutoDescriptor()







class ScriptKind:
    """
    Identify/link the macros with their needs in terms of JS scripts to add to the page
    (not in the headers/footers)
    """
    pyodide = AutoDescriptor()
    terms = AutoDescriptor()
    ides = AutoDescriptor()
    qcm = AutoDescriptor()

    # content = AutoDescriptor()        # not used anymore => forbid it
    libs = AutoDescriptor()
    scripts = AutoDescriptor()
    extrahead = AutoDescriptor()


    @staticmethod
    def is_page_related(kind:str):
        """
        Identify if the given identifier is a ScriptKind to insert for a specific macro.
        """
        return kind in PAGES_KINDS

    @staticmethod
    def is_main_related(kind:str):
        """
        Identify if the given identifier is a Script to in sert in a block of main.html.
        """
        return kind in BLOCKS_KINDS

    @staticmethod
    def is_to_insert(kind:str):
        """
        Identify if the given identifier is a Script to in sert in a block of main.html.
        """
        return kind in INSERTIONS_KINDS


KIND_ORDER = {
    ScriptKind.libs: -10,
    ScriptKind.extrahead: 0,

    ScriptKind.pyodide: 1,
    ScriptKind.terms: 2,
    ScriptKind.ides: 3,
    ScriptKind.qcm: 10,

    ScriptKind.scripts: 100,
}


BLOCKS_KINDS = set('content libs scripts extrahead'.split())
INSERTIONS_KINDS = {s for s in dir(ScriptKind) if not s.startswith('_')
                                               and not callable(getattr(ScriptKind, s)) }
PAGES_KINDS = INSERTIONS_KINDS - BLOCKS_KINDS





class DebugConfig(Namespace):

    check_decode = False
    """ If True, decode any LZW encoded string to check consistency """
