# fsync/__init__.py

"""
FSync: local file synchronization tool.

Keeps scattered copies of shared libraries in sync across projects.
Works as CLI (`py -m fsync`), pip-installed command (`fsync`),
or importable module.

Example:
  >>> from fsync.main import main
  >>> from fsync.utils import backup_file
  >>> from fsync.diff import show
"""

__version__ = "1.0.1"
__repo__ = "Xaeian/FSync"
__python__ = ">=3.12"
__description__ = "Local file synchronization for scattered shared libraries"
__author__ = "Xaeian"
__keywords__ = ["sync", "files", "libraries", "backup"]
__dependencies__ = ["xaeian"]
__scripts__ = {
  "pyfsync": "fsync.__main__:main",
}

from .utils import backup_file, BACKUP_DIR, BACKUP_KEEP

__all__ = [
  "backup_file", "BACKUP_DIR", "BACKUP_KEEP",
]