# -*-codeing:utf-8-*-
import os
import sys
from distutils.core import setup
import py2exe

#
# setup(console=['RunWeb.py','TestServer.py','runTest.py','recorder.py'])

# this allows to run it with a simple double click.
sys.argv.append('py2exe')

py2exe_options = {
    "includes": ["sip"],
    "dll_excludes": ["MSVCP90.dll", "MSVCR80.dll", "oci.dll"],
    "compressed": 1,
    "optimize": 2,
    "ascii": 0,
}

serverlib = []
for files in os.listdir('Q:\\AiTest\\'):
    f = 'Q:\\AiTest\\' + files
    if os.path.isfile(f):
        serverlib.append(f)

setup(
    name='PyQt Demo',
    version='1.0',
    windows=['recorder.py',{"script": "TestStart.py", "icon_resources": [(1, "TestStart.ico")]}],
    console=['RunWeb.py', 'TestServer.py', 'runTest.py'],
	data_files=[("", ['DevSqlMapConfig.xml', 'IEDriverServer.exe', 'config.ini', 'TestServer.bat',
                       'oci.dll']), ("temp", ['temp\AT_AFTER_CASE.py',
                                                                                         'temp\AT_AFTER_TEST.py',
                                                                                         'temp\AT_BEFORE_CASE.py',
                                                                                         'temp\AT_BEFORE_TEST.py',
                                                                                         'temp\AT_ERROR_CASE.py']),
                 ("logs", []),
                 ("out_sql", []), ("cases", [])], 
      #("serverlib", serverlib),
    zipfile=None, 
    options={'py2exe': py2exe_options}
)
