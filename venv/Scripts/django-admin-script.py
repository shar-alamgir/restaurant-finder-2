#!c:\users\marcus~1\desktop\cs411\rf2\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Django','console_scripts','django-admin'
__requires__ = 'Django'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Django', 'console_scripts', 'django-admin')()
    )
