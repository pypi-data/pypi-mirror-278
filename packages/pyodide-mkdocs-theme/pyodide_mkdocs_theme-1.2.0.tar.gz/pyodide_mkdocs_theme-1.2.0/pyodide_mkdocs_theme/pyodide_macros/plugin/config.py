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


from mkdocs.config import config_options as C
from mkdocs_macros.plugin import MacrosPlugin

from .maestro_tools import CopyableConfig, DeprecatedMsg, deprecated_option
from ..macros.macros_args_config import ARGS_MACRO_CONFIG




# Verify if something changed on the MacrosPlugin side... (moved to on_startup)
# Current setup for MacrosPlugin v1.0.4

_EXPECTED_MACRO_CONF = set("""
    module_name
    modules
    render_by_default
    include_dir
    include_yaml
    j2_block_start_string
    j2_block_end_string
    j2_variable_start_string
    j2_variable_end_string
    on_undefined
    on_error_fail
    verbose
""".split())

_SRC_MACROS_CONF = dict(MacrosPlugin.config_scheme)

_MISSING_MACROS_PLUGIN_PROPS = _EXPECTED_MACRO_CONF - set(_SRC_MACROS_CONF)
MISSING_MACROS_PROPS = (
    "" if not _MISSING_MACROS_PLUGIN_PROPS else "\nDisappeared from MacrosPlugin:" + ''.join(
        f'\n\t{name}' for name in _MISSING_MACROS_PLUGIN_PROPS
    )
)

_NEW_MACROS_PLUGIN_PROPS = set(_SRC_MACROS_CONF) - _EXPECTED_MACRO_CONF
EXTRAS_MACROS_PROPS = (
    "" if not _NEW_MACROS_PLUGIN_PROPS else "\nNew config in MacrosPlugin:" + ''.join(
        f'\n\t{name}' for name in _NEW_MACROS_PLUGIN_PROPS
    )
)


J2_STRING                  = _SRC_MACROS_CONF['include_dir'].default
DEFAULT_MODULE_NAME        = _SRC_MACROS_CONF['module_name'].default
DEFAULT_UNDEFINED_BEHAVIOR = _SRC_MACROS_CONF['on_undefined'].default







class BuildConfig(CopyableConfig):
    """ Build configuration options """

    ignore_macros_plugin_diffs = C.Type(bool, default=False)
    """
    Set to True to bypass the compatibility check of the `PyodideMacrosPlugin` config against
    the original `MacrosPlugin` one.

    ??? note "Reasons behind this verification"

        `MacrosPlugin` is configured the "old fashion" way while `PyodideMacrosPlugin` is using
        mkdocs 1.5+ Config classes. This means that the `MacrosPlugin` configuration had to be
        hardcoded in the `PyodideMacrosPlugin` config.

        Because of this, any config change on the `MacrosPlugin` side could break
        `PyodideMacrosPlugin` without warning, so this verification enforce the expected
        implementation of the parent class.

        If ever something unexpected is found, the build will be aborted, because no guarantee
        can be given about the correctness of the build in such a situation.

        In case of minor changes, this option will allow the build, but use it "at your own risks".
    """

    forbid_macros_override = C.Type(bool, default=True)
    """
    If True, `PyodideMacrosError` is raised when two macros are registered with the same name.
    """

    skip_py_md_paths_names_validation = C.Type(bool, default=False)
    """
    By default, the path names of all the `.py` and `.md` files present in the docs_dir are
    checked so that they do not contain any character other than letters, digits, dot or dash.
    This ensures that the macros related to IDEs will work properly.

    If unwanted characters are found, a BuildError is raised, but this verification can be turned
    off by setting this flag to True. Use it at your own risks.
    """

    python_libs = C.ListOfItems(C.Type(str), default=['py_libs'])
    """
    Personal python packages directories to use on the built site.

    * Invalid names are ignored during the build.
    * A warning will be emitted, unless it's the default directory that is missing (`#!py 'py_libs'`).
    * The libraries have to be ___directories___ in the project directory (_not_ the docs_dir).
    """

    load_yaml_encoding = C.Type(str, default='utf-8')
    """
    Encoding to use when loading yaml data with the original MacrosPlugin functionalities :

    The original method doesn't use any encoding argument, which can lead to different behaviors
    between Windows and Linux (typically: during a pipeline!).
    """

    macros_with_indents = C.ListOfItems(C.Type(str), default=[])
    """
    Allow to register external macros, as a list of strings, that will need to insert properly
    indented multiline contents in the page.

    This is relying on `PyodideMacrosPlugin.get_indent` logistic.
    """

    meta_yaml_encoding = C.Type(str, default='utf-8')
    """ Encoding to use when loading meta.pmt.yml files. """

    _pmt_meta_filename = C.Type(str, default=".meta.pmt.yml")
    """ Name used for the Pyodide MkDoc Theme meta files. """


    #----------------------------------------------------------------------------


    encrypt_corrections_and_rems = deprecated_option(
        'ides.encrypt_corrections_and_rems', bool, DeprecatedMsg.moved
    )
    """
    If True, the html div under IDEs containing correction and remarks will be encrypted at build
    time.

    Passing this to False can be useful during development, but value should _ALWAYS_ be set
    to true on the deployed website: keep in mind the search engine can otherwise make surface
    contents from corrections and remarks as suggestions when the user is using the search bar.
    """

    forbid_secrets_without_corr_or_REMs = deprecated_option(
        'ides.forbid_secrets_without_corr_or_REMs', bool, DeprecatedMsg.moved
    )
    """
    By default, this situation is considered invalid and `BuildError` will be raised.
    If this is the desired behavior, set this option to false.
    """

    forbid_hidden_corr_and_REMs_without_secrets = deprecated_option(
        'ides.forbid_hidden_corr_and_REMs_without_secrets', bool, DeprecatedMsg.moved
    )
    """
    When building IDEs, the validation button will appear only when a `secrets` section exist.
    If none is given while a corr section or REM files exist, their content will never be available
    to the user because of the lack of validation button in the interface.

    By default, this situation is considered invalid and `BuildError` will be raised.
    If this is the desired behavior, set this option to false.
    """

    forbid_corr_and_REMs_with_infinite_attempts = deprecated_option(
        'ides.forbid_corr_and_REMs_with_infinite_attempts', bool, DeprecatedMsg.moved
    )
    """
    When building IDEs, if a `corr` section, a REM file or a VIS_REM file exist while the number
    of attempts is infinite, that content will never become accessible to the user, unless they
    pass the tests.

    By default, this situation is considered invalid and `BuildError` will be raised.
    If this is the desired behavior, set this option to false.
    """

    bypass_indent_errors = deprecated_option('bypass_indent_errors', bool, DeprecatedMsg.removed)
    """
    _DEPRECATED: This option shouldn't be needed anymore._

    If True, all errors raised when trying to find what is the indentation level of a macro call
    are bypassed and a message is instead printed to the console.

    The purpose of this option is _not_ to deactivate the securities, but to allow gathering info
    about all the indentation problems at once: the resulting markdown content will most likely be
    incorrect and be rendered with unexpected results.
    """

    # check_python_files = C.Type(bool, default=False)
    # """
    # If True, the different sections of the python files will be tested against each others during
    # the build and provide feedback in the console.

    # Unless the `soft_check` option is used, a BuildError will be raised if something considered
    # wrong happens. See the documentation for more details.

    # Warning:
    #     - This is totally independent from the pyodide environment. For example, it won't
    #       give any warning if a forbidden function is used in the tests (which will fail
    #       on the website).
    #     - These verifications __considerably increase the build time__ (expect something
    #       around x10).
    # """

    # soft_check = C.Type(bool, default=True)
    # """
    # If True and `check_python_files` is also True, the python sections are verified, but the
    # build won't be interrupted if something wrong or suspicious is discovered: a message will
    # instead be displayed in the console.
    # """





class IdeConfig(CopyableConfig):
    """ All options related to validation tests (IDEs) """

    encrypt_corrections_and_rems = C.Type(bool, default=True)
    """
    If True, the html div under IDEs containing correction and remarks will be encrypted at build
    time.

    Passing this to False can be useful during development, but value should _ALWAYS_ be set
    to true on the deployed website: keep in mind the search engine can otherwise make surface
    contents from corrections and remarks as suggestions when the user is using the search bar.
    """

    encrypt_alpha_mode = C.Choice(('shuffle', 'direct', 'sort'), default='direct')
    """
    Determine how the alphabet for the LZW compression is built, from the content to encode:

    - `"shuffle"`: the alphabet is randomized.
    - `"direct"`: the alphabet is using all symbols in order.
    - `"sort"`: the alphabet sorting all symbols in natural order.
    """

    forbid_secrets_without_corr_or_REMs = C.Type(bool, default=True)
    """
    By default, this situation is considered invalid and `BuildError` will be raised.
    If this is the desired behavior, set this option to false.
    """

    forbid_hidden_corr_and_REMs_without_secrets = C.Type(bool, default=True)
    """
    When building IDEs, the validation button will appear only when a `secrets` section exist.
    If none is given while a corr section or REM files exist, their content will never be available
    to the user because of the lack of validation button in the interface.

    By default, this situation is considered invalid and `BuildError` will be raised.
    If this is the desired behavior, set this option to false.
    """

    forbid_corr_and_REMs_with_infinite_attempts = C.Type(bool, default=True)
    """
    When building IDEs, if a `corr` section, a REM file or a VIS_REM file exist while the number
    of attempts is infinite, that content will never become accessible to the user, unless they
    pass the tests.

    By default, this situation is considered invalid and `BuildError` will be raised.
    If this is the desired behavior, set this option to false.
    """

    decrease_attempts_on_user_code_failure = C.Type(bool, default=True)
    """
    If true, any failure when running the user code during a validation will decrease the number
    of attempts left. Note this means even syntax errors will decrease the count.

    When this option is set to True, any error raised within the code of the editor will stop
    the validation process without modifying the number of attempts left.
    """

    deactivate_stdout_for_secrets = C.Type(bool, default=True)
    """
    Define if the stdout will be shown to the user or not, for the secret tests.
    """

    show_only_assertion_errors_for_secrets = C.Type(bool, default=False)
    """
    If True, the stack trace of all error messages will be suppressed and only assertion messages
    will be left unchanged, when an error is raised during the secret tests.
    """

    #--------------------------------------------------------------------------------


    show_assertion_code_on_failed_test = deprecated_option('args.IDE.LOGS',bool,DeprecatedMsg.moved)
    """
    When an assertion fails in the secret tests and that assertion doesn't have any assertion
    message, the code of the assertion itself will be displayed in the terminal if this option
    is set to True (default).

    This behavior is global, but can be overridden on a "per IDE" base, using the `auto_log_assert`
    optional argument.
    """

    max_attempts_before_corr_available = deprecated_option('args.IDE.MAX',int, DeprecatedMsg.moved)
    """
    Global setting for all IDE in the documentation: max number of tries a user can do before
    correction and remarks become available (reminder: they are in a collapsed details/admonition,
    requiring the user to click to reveal the content. This way, they can still try to get the code
    right without actually seeing the solution, before actually giving up).

    NOTE: using 1000 will result in an infinite number of attempts (ie. corr and REMs contents will
    never become available if any).

    This behavior is global, but can be overridden on a "per IDE" base, using the `MAX` optional
    argument.
    """

    default_ide_height_lines = deprecated_option('args.IDE.MAX_SIZE', int, DeprecatedMsg.moved)
    """
    Max height of the editor (in number of lines). For the macro IDEv, this takes precedence on
    the TERM_H argument of the terminal.
    """





class TermConfig(CopyableConfig):
    """ Terminals configuration options """

    stdout_cut_off = C.Type(int, default=200)
    """
    Maximum number of lines displayed at once in a terminal. If more lines are printed, the
    lines at the top are removed.

    NOTE: jQuery.terminals become AWFULLY SLOW when the number of characters they display
    become somewhat massive. This option allows to limit these performances troubles, when
    the stdout is not truncated (see terminals upper right corner button). Also note that
    this option _does not_ limit the number of characters per line, so a frozen page can
    still occur, while the truncation feature will take care of that.
    """

    #--------------------------------------------------------------------------------

    default_height_ide_term = deprecated_option('args.IDE.TERM_H', int, DeprecatedMsg.moved)
    """
    Default height value (number of lines) for terminals in IDEs.
    """

    default_height_isolated_term = deprecated_option('args.terminal.TERM_H', int, DeprecatedMsg.moved)
    """
    Default height value (number of lines) for isolated terminals.
    """






class QcmsConfig(CopyableConfig):
    """ Options specific to the QCMs or QCSs"""

    hide = deprecated_option('args.multi_qcm.hide', bool, DeprecatedMsg.moved)
    """
    Global choice for the `shuffle` argument of QCMs.
    """

    multi =  deprecated_option('args.multi_qcm.multi', bool, DeprecatedMsg.moved)
    """
    Global choice for the `multi` argument.

    If this option is set to `True` or `False`, it will act as a documentation-wide setting to
    disambiguate questions having 0 or 1 correct answers only.
    """

    shuffle = deprecated_option('args.multi_qcm.shuffle', bool, DeprecatedMsg.moved)
    """
    Global choice for the `shuffle` argument of QCMs.
    """






class OtherConfig(CopyableConfig):
    """ Options used in the macros that have not been updated yet """

    scripts_url = deprecated_option('scripts_url', str, DeprecatedMsg.unsupported_macro)
    site_root   = deprecated_option('site_root', str, DeprecatedMsg.unsupported_macro)






# This only defines the values exposed to the user in mkdocs.yml.
# When a property is declared here, don't forgot to add the related extractor on the
# BaseMaestro class.
class PyodideMacrosConfig(CopyableConfig):
    """ Configuration for the main pyodide-mkdocs-theme plugin. """

    _dev_mode = C.Type(bool, default=False)
    """ Run the plugin in development mode (...don't use that). """

    build = C.SubConfig(BuildConfig)
    """ Build related options """

    ides = C.SubConfig(IdeConfig)
    """ Configuration related to the validation tests in IDEs """

    terms = C.SubConfig(TermConfig)
    """ Configuration related to the terminals """

    qcms = C.SubConfig(QcmsConfig)
    """ QCMs related options """

    _others = C.SubConfig(OtherConfig)
    """ Old configuration options (unmaintained, so far) """

    args = ARGS_MACRO_CONFIG.to_config()
    """ Macros arguments configuration (see use of `.met.pmt.yml` files and metadata headers). """

    # ---------------------------------------------------------------------------------------
    # Replication of MacrosPlugin options (merging the config_scheme properties programmatically
    # is not enough, unfortunately...)


    render_by_default        = C.Type(bool, default=True)
    """
    Render macros on all pages by default. If set to false, sets an opt-in mode where only pages
    marked with render_macros: true in header will be displayed.
    """
    module_name              = C.Type(str,  default=DEFAULT_MODULE_NAME)
    """
    Name of the Python module containing macros, filters and variables. Indicate the file or
    directory, without extension; you may specify a path (e.g. include/module). If no main
    module is available, it is ignored.
    """
    modules                  = C.Type(list, default=[])
    """
    List of pluglets to be added to mkdocs-macros (preinstalled Python modules that can be listed
    by pip list).
    """
    include_dir              = C.Type(str,  default=J2_STRING)
    """ Directory for including external files """
    include_yaml             = C.Type(list, default=[])
    """ Non-standard Jinja2 marker for start of block """
    j2_block_start_string    = C.Type(str,  default=J2_STRING)
    """ Non-standard Jinja2 marker for start of variable """
    j2_block_end_string      = C.Type(str,  default=J2_STRING)
    """ Non-standard Jinja2 marker for end of block """
    j2_variable_start_string = C.Type(str,  default=J2_STRING)
    """ Non-standard Jinja2 marker for end of variable """
    j2_variable_end_string   = C.Type(str,  default=J2_STRING)
    """ Non-standard Jinja2 marker for end of variable """
    on_error_fail            = C.Type(bool, default=False)
    """
    Make the building process fail in case of an error in macro rendering (this is useful when
    the website is rebuilt automatically and errors must be detected.)
    """
    on_undefined             = C.Type(str,  default=DEFAULT_UNDEFINED_BEHAVIOR)
    """
    Behavior of the macros renderer in case of an undefined variable in a page. By default, it
    leaves the Jinja2 statement untouched (e.g. {{ foo }} will appear as such in the page.) Use
    the value 'strict' to make it fail.
    """
    verbose                  = C.Type(bool, default=False)
    """ Print debug (more detailed) statements in the console. """
