# fsync/utils.py

import os
from datetime import datetime
from xaeian import FILE, DIR, PATH

BACKUP_DIR = "backups"
BACKUP_KEEP = 10

def _find_backups(name: str) -> list[str]:
  """Find all backups for given sync name, sorted oldest first."""
  dir = PATH.resolve(f"{BACKUP_DIR}/{name}")
  if not os.path.isdir(dir): return []
  return [f"{dir}/{f}" for f in sorted(os.listdir(dir))]

def backup_file(path: str, name: str) -> bool:
  """
  Backup file before overwriting.
  Layout: backups/ary.c/2025-02-24@14-30-00.c
  Skips if identical to latest backup. Rotates beyond BACKUP_KEEP.
  """
  file_hash = FILE.hash(path, algo="md5")
  existing = _find_backups(name)
  if existing and FILE.hash(existing[-1], algo="md5") == file_hash:
    return False
  dir = PATH.resolve(f"{BACKUP_DIR}/{name}")
  DIR.ensure(f"{dir}/")
  ext = PATH.ext(name)
  stamp = datetime.now().strftime("%Y-%m-%d@%H-%M-%S")
  dst = f"{dir}/{stamp}{ext}"
  DIR.copy(path, dst)
  # Rotate
  all_backups = _find_backups(name)
  while len(all_backups) > BACKUP_KEEP:
    os.remove(all_backups.pop(0))
  return True