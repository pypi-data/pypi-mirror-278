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

import sys
from pathlib import Path
from argparse import ArgumentParser
from contextlib import redirect_stdout


from .__version__ import __version__

PMT_SCRIPTS = 'scripts'



parser = ArgumentParser(
    'pyodide_mkdocs_theme',
    description = "Scripts for pyodide-mkdocs-theme",
    epilog = "Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli. "
             "This program comes with ABSOLUTELY NO WARRANTY."
)
parser.add_argument(
    '-V', '--version', action='version', version=f'pyodide-mkdocs-theme {__version__}'
)
parser.add_argument(
    '--lang', action='store_true', help='Print the base python code to customize some messages'
)
parser.add_argument(
    '--mime', action='store_true', help='Open a page in the browser, to the MDN documentation about MIME types'
)
parser.add_argument(
    '--py', action='store_true', help='Print an example of python file, for {{IDE(...)}} or {{terminal(...)}} macros'
)
parser.add_argument(
    '--yml', action='store_true', help='Print a base configuration for the mkdocs.yml file'
)
parser.add_argument(
    '-F', '--file', default="",
    help='Use this argument to write the information into a file instead of the stdout '
         '(existing content will be overridden. Use an absolute path or a path relative to the cwd)'
)



def main():
    # pylint: disable=multiple-statements

    if len(sys.argv) < 2:
        sys.argv.append('-h')

    args = parser.parse_args()

    if args.mime:
        import webbrowser
        webbrowser.open("https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types", new=2)
        return


    def display(filename:str):
        """ Display the base code for GUI messages customizations """

        src = Path(__file__).parent / PMT_SCRIPTS / filename
        txt = src.read_text(encoding='utf-8')
        print(txt)


    def inner():
        if args.lang:   display('custom_lang.py')
        elif args.yml:  display('mkdocs.yml')
        elif args.py:   display('model.py')


    if not args.file:
        inner()

    else:
        path = Path(args.file)
        path.touch(exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f, redirect_stdout(f):
            inner()



if __name__ == '__main__':
    main()
