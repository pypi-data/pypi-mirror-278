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
# pylint: disable=multiple-statements


from functools import wraps
import re
import json
from typing import List, Optional
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import BuildError
from mkdocs.structure.pages import Page
from mkdocs.plugins import BasePlugin

from ...__version__ import __version__
from ..tools_and_constants import ICONS_IN_TEMPLATES_DIR
from ..exceptions import PyodideMacrosError
from ..messages import Lang
from ..pyodide_logger import logger
from .maestro_tools import ConfigExtractor, dump_and_dumper
from .config import PyodideMacrosConfig








class BaseMaestro(BasePlugin[PyodideMacrosConfig]):
    """
    Main class, regrouping the basic configurations, properties, getters and/or constants
    for the different children classes: each of them will inherit from MaestroConfig.
    It is also used as "sink" for the super calls of other classes that are not implemented
    on the MacrosPlugin class.

    Note that, for the ConfigExtractor for to properly work, the class hierarchy has to
    extend MacrosPlugin at some point.
    """

    ignore_macros_plugin_diffs:         bool = ConfigExtractor('build')
    forbid_macros_override:             bool = ConfigExtractor('build')
    skip_py_md_paths_names_validation:  bool = ConfigExtractor('build')
    load_yaml_encoding:                 str  = ConfigExtractor('build')
    meta_yaml_encoding:                 str  = ConfigExtractor('build')
    macros_with_indents:           List[str] = ConfigExtractor('build')
    python_libs:                   List[str] = ConfigExtractor('build')
    _pmt_meta_filename:                 str  = ConfigExtractor('build')

    decrease_attempts_on_user_code_failure:           bool = ConfigExtractor("ides")
    deactivate_stdout_for_secrets:          Optional[bool] = ConfigExtractor("ides")
    encrypt_alpha_mode:                                str = ConfigExtractor("ides")
    encrypt_corrections_and_rems:                     bool = ConfigExtractor('ides')
    forbid_secrets_without_corr_or_REMs:              bool = ConfigExtractor('ides')
    forbid_hidden_corr_and_REMs_without_secrets:      bool = ConfigExtractor('ides')
    forbid_corr_and_REMs_with_infinite_attempts:      bool = ConfigExtractor('ides')
    show_only_assertion_errors_for_secrets: Optional[bool] = ConfigExtractor("ides")

    stdout_cut_off: int = ConfigExtractor("terms")


    scripts_url: str = ConfigExtractor("_others")
    site_root:   str = ConfigExtractor("_others")


    # global mkdocs config data:
    docs_dir:    str = ConfigExtractor(root='_conf')
    repo_url:    str = ConfigExtractor(root='_conf')
    site_name:   str = ConfigExtractor(root='_conf')
    site_url:    str = ConfigExtractor(root='_conf')
    site_dir:    str = ConfigExtractor(root='_conf')

    # Specific to the original macros plugin:
    _dev_mode:               bool = ConfigExtractor()
    j2_block_start_string:    str = ConfigExtractor()
    j2_block_end_string:      str = ConfigExtractor()
    j2_variable_start_string: str = ConfigExtractor()
    j2_variable_end_string:   str = ConfigExtractor()


    # ARGS EXTRACTOR TOKEN
    args_IDE_py_name: str = ConfigExtractor('args.IDE', prop='py_name')
    args_IDE_SANS: str = ConfigExtractor('args.IDE', prop='SANS')
    args_IDE_WHITE: str = ConfigExtractor('args.IDE', prop='WHITE')
    args_IDE_REC_LIMIT: int = ConfigExtractor('args.IDE', prop='REC_LIMIT')
    args_IDE_MAX: int = ConfigExtractor('args.IDE', prop='MAX')
    args_IDE_LOGS: bool = ConfigExtractor('args.IDE', prop='LOGS')
    args_IDE_MAX_SIZE: int = ConfigExtractor('args.IDE', prop='MAX_SIZE')
    args_IDE_TERM_H: int = ConfigExtractor('args.IDE', prop='TERM_H')
    args_terminal_py_name: str = ConfigExtractor('args.terminal', prop='py_name')
    args_terminal_SANS: str = ConfigExtractor('args.terminal', prop='SANS')
    args_terminal_WHITE: str = ConfigExtractor('args.terminal', prop='WHITE')
    args_terminal_REC_LIMIT: int = ConfigExtractor('args.terminal', prop='REC_LIMIT')
    args_terminal_TERM_H: int = ConfigExtractor('args.terminal', prop='TERM_H')
    args_terminal_FILL: str = ConfigExtractor('args.terminal', prop='FILL')
    args_py_btn_py_name: str = ConfigExtractor('args.py_btn', prop='py_name')
    args_py_btn_SANS: str = ConfigExtractor('args.py_btn', prop='SANS')
    args_py_btn_WHITE: str = ConfigExtractor('args.py_btn', prop='WHITE')
    args_py_btn_REC_LIMIT: int = ConfigExtractor('args.py_btn', prop='REC_LIMIT')
    args_py_btn_WRAPPER: str = ConfigExtractor('args.py_btn', prop='WRAPPER')
    args_py_btn_HEIGHT: int = ConfigExtractor('args.py_btn', prop='HEIGHT')
    args_py_btn_WIDTH: int = ConfigExtractor('args.py_btn', prop='WIDTH')
    args_py_btn_SIZE: int = ConfigExtractor('args.py_btn', prop='SIZE')
    args_py_btn_ICON: str = ConfigExtractor('args.py_btn', prop='ICON')
    args_py_btn_TIP: str = ConfigExtractor('args.py_btn', prop='TIP')
    args_py_btn_TIP_SHIFT: int = ConfigExtractor('args.py_btn', prop='TIP_SHIFT')
    args_py_btn_TIP_WIDTH: float = ConfigExtractor('args.py_btn', prop='TIP_WIDTH')
    args_section_py_name: str = ConfigExtractor('args.section', prop='py_name')
    args_section_section: str = ConfigExtractor('args.section', prop='section')
    args_multi_qcm_hide: bool = ConfigExtractor('args.multi_qcm', prop='hide')
    args_multi_qcm_multi: bool = ConfigExtractor('args.multi_qcm', prop='multi')
    args_multi_qcm_shuffle: bool = ConfigExtractor('args.multi_qcm', prop='shuffle')
    args_multi_qcm_admo_kind: str = ConfigExtractor('args.multi_qcm', prop='admo_kind')
    args_multi_qcm_admo_class: str = ConfigExtractor('args.multi_qcm', prop='admo_class')
    args_multi_qcm_qcm_title: str = ConfigExtractor('args.multi_qcm', prop='qcm_title')
    args_multi_qcm_DEBUG: bool = ConfigExtractor('args.multi_qcm', prop='DEBUG')
    args_py_py_name: str = ConfigExtractor('args.py', prop='py_name')
    # ARGS EXTRACTOR TOKEN


    #----------------------------------------------------------------------------
    # WARNING: the following properties are assigned from "other places":
    #   - pages from the original MacrosPlugin
    #   - others from PyodideMacrosPlugin

    page: Page  # just as a reminder: defined by MacrosPlugin

    docs_dir_path: Path
    """ Current docs_dir of the project as a Path object (ABSOLUTE path) """

    docs_dir_cwd_rel: Path
    """ docs_dir Path object, but relative to the CWD, at runtime """

    _macro_with_indent_pattern:re.Pattern = None
    """
    Pattern to re.match macro calls that will need to handle indentation levels.
    Built at runtime (depends on `macro_with_indents`)
    """

    #----------------------------------------------------------------------------
    # Transferred to JS CONFIG:

    base_url:str = ""
    button_icons_directory:str = ""
    pmt_url:str = 'https://gitlab.com/frederic-zinelli/pyodide-mkdocs-theme'
    version:str = __version__
    lang: Lang = None




    # Override MacroPlugin
    def on_config(self, config:MkDocsConfig):       # pylint: disable=missing-function-docstring

        self.lang = Lang()
        self.lang.register_env(self)

        if self.skip_py_md_paths_names_validation:
            logger.warning("skip_py_md_paths_names_validation option is activated.")

        super().on_config(config)   # pylint: disable-next=no-member
                                    # MacrosPlugin is actually "next in line" and has the method


    # Override MacroPlugin
    def macro(self, func, name=""):     # pylint: disable=arguments-renamed
        """
        Add an extra wrapper around the macro, so that the different classes can inject
        their logic around the macros calls themselves, when needed.
        """
        name = name or func.__name__
        if self.forbid_macros_override and name in self.macros:
            raise PyodideMacrosError(f'A macro named "{name}" has already been registered')
            # Note: the macro plugin creates a fresh dict on each _on_config hook.

        @wraps(func)
        def wrapper(*a,**kw):
            return self.apply_macro(name, func, *a, **kw)

        wrapper.__name__ = wrapper.__qualname__ = name
        return super().macro(wrapper, name)


    def apply_macro(self, name, func, *a, **kw):            # pylint: disable=unused-argument
        """ Root method: just call the macro... """
        return func(*a, **kw)


    #----------------------------------------------------------------------------


    def location(self, page:Optional[Page]=None):
        """ Path to the current file, relative to the cwd. """
        page = page or getattr(self, 'page', None)
        if not page:
            raise BuildError("No page defined yet")
        return f"{ self.docs_dir_cwd_rel }/{ page.file.src_uri }"


    def level_up_from_current_page(self, url:str=None) -> str:
        """
        Return the appropriate number of ".." steps needed to build a relative url to go from the
        current page url back to the root directory.

        Note there are no trailing backslash.

        @url: relative to the docs_dir (ex: "exercices/ ..."). If None, use self.page.url instead.
        """
        url = self.page.url if url is None else url
        page_loc:Path = self.docs_dir_path / url
        segments = page_loc.relative_to(self.docs_dir_path).parts
        out = len(segments) * ['..']
        return '/'.join(out) or '.'


    #----------------------------------------------------------------------------


    def rebase(self, base_url:str):
        """
        Necessary for development only (to replace the wrong base_url value during a serve in the
        theme project)
        NOTE: Keep in mind the base_url SOMETIMES ends with a slash...
        """
        return base_url if base_url!='/' else '.'


    def dump_to_js_config(self, base_url):
        """
        Create the <script> tag that will add all the CONFIG properties needed in the JS
        global config file, and also applies the post conversion where needed.
        """
        to_dump = 'base_url button_icons_directory pmt_url version'.split()

        # HACK!
        # This method can be called with self being None to build the placeholder CONFIG in
        # 0_config-libs.js, si fill the data only when self actually exists.
        if self:                                # pylint: disable=w0201
            if self._dev_mode:
                to_dump.append('_dev_mode')
            base_url = self.rebase(base_url).rstrip('/')
            self.button_icons_directory = f"{base_url}/{ICONS_IN_TEMPLATES_DIR}"
            self.base_url = base_url

        dct = dump_and_dumper(to_dump, self, json.dumps)

        # Add the Lang dump (which requires a slightly different logic):
        dct['lang'] = Lang.dump_as_str(self and self.lang)

        if self:                        # HACK!
            # Dump to main.htm, then adding post conversions operations:
            dumping = [ f"\n  CONFIG.{ prop } = { val }" for prop,val in dct.items() ]
            dumped = f'''\
<script type="application/javascript">
{ "".join(dumping) }
CONFIG.lang.tests.as_pattern = new RegExp(CONFIG.lang.tests.as_pattern, 'i')
</script>'''

        else:
            # Dump the placeholders to the JS config-libs file:
            dumping = [ f"\n    { prop }: { val }," for prop,val in dct.items() ]
            dumped = ''.join(dumping)

        return dumped


    #----------------------------------------------------------------------------


    def _omg_they_killed_keanu(self,page_name:str, page_on_context:Page=None):
        """ Debugging purpose only. Use as breakpoint utility.
            @page_on_context argument used when called "outside" of the macro logic (fro example,
            in external hooks)
        """
        page = page_on_context or self.page
        if page_name == page.url:
            logger.error("Breakpoint! (the CALL to this method should be removed)")


    def warn_unmaintained(self, that:str):
        """
        Generic warning message for people trying to used untested/unmaintained macros.
        """
        logger.warning(
            f"{ that.capitalize() } has not been maintained since the original pyodide-mkdocs "
            "project, may not currently work, and will be removed in the future.\n"
            "Please open an issue on the pyodide-mkdocs-theme repository, if you need it.\n\n"
            f"\t{ self.pmt_url }"
        )
