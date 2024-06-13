from typing import LiteralString, List

# Regex pattern for match single line HTML tags used by `PyHtml`
RE_HTML_PATTERN: LiteralString

# Supported HTML file extensions that `setup` looks for
HTML_FILE_EXTENSIONS: List[str]

# All file extensions that `setup` looks for
FILE_EXTENSIONS: List[str]

# Used for backwards compatibility with Python versions below 3.12. Older versions 
# raise a SyntaxError when you try to include a plain backslash in an f-string, like: f"{'\\'}". 
# Using a constant instead, like: f"{BACKSLASH}" circumvents this problem.
BACKSLASH: LiteralString

# This is stored as a constant to make it easy to change in the future. (If Needed)
SYS_BUNDLE_ATTRIBUTE: LiteralString

# Basic HTML Template, used as a fallback for `pywebview`
HTML_TEMPLATE: LiteralString

# Supported Image Extensions
IMAGE_FILE_EXTENSIONS: List[str]

# The name the ralium api uses for storing exposed functions
RALIUM_API_REGISTRY_IDENTIFIER: LiteralString

# The prefix used for creating ralium element ids
RALIUM_ID_IDENTIFIER_PREFIX: LiteralString

# A list of all HTML Elements
ALL_HTML_ELEMENTS: List[str]

# A list of all methods attached to elements
ALL_HTML_ELEMENT_INSTANCE_METHODS: List[str]