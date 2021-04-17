"""
Contains regexp-s.
"""

import re


url_regexp = r'''((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'''
url_pattern = re.compile(url_regexp)
