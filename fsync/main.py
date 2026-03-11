# fsync/main.py

"""
FSync: file synchronization engine.

Core sync logic: load workspace, resolve paths, detect
changes, update obsolete files with backup rotation.

Example:
  >>> from fsync.main import main
  >>> main()
"""

import os, sys
from datetime import datetime
from xaeian import JSON, INI, FILE, DIR, PATH, replace_map, Ico, Print, Color as c
from xaeian.files import set_context
from .args import load_args
from . import __version__, __repo__

WORKSPACE_FILE = PATH.expand("~/.fsync.txt")

def main():
  p = Print()
  args = load_args()

  if args.version:
    print(f"FSync {c.BLUE}{__version__}{c.END}")
    print(f"Repo: {c.GREY}https://{c.END}github.com/{__repo__}")
    sys.exit(0)

  #------------------------------------------------------------------------------------- Workspace
  if args.workspace is not None:
    ws = os.path.abspath(PATH.expand(args.workspace))
    if not PATH.is_dir(ws):
      p.err(f"Directory {c.GREY}{ws}{c.END} doesn't exist")
      sys.exit(1)
    FILE.save(WORKSPACE_FILE, ws)
    p.ok(f"Set directory {c.ORANGE}{ws}{c.END} as workspace")
    if not any([args.update, args.info, args.example, args.diff]):
      sys.exit(0)

  if not PATH.is_file(WORKSPACE_FILE):
    p.err(f"No workspace set. Use {c.GREY}-w --workspace{c.END} to set one")
    sys.exit(1)
  workspace = FILE.load(WORKSPACE_FILE).strip()
  if not PATH.is_dir(workspace):
    p.err(f"Workspace {c.ORANGE}{workspace}{c.END} doesn't exist")
    sys.exit(1)

  set_context(root_path=workspace)

  if args.example:
    from . import example
    example.create()
    sys.exit(0)

  #---------------------------------------------------------------------------------------- Config
  
  sync = JSON.load("sync.json")
  if not sync:
    p.err(f"Missing or invalid {c.RED}sync.json{c.END}")
    sys.exit(1)
  sync = {k: v for k, v in sync.items() if not k.startswith("#")}
  if not sync:
    p.err(f"No active entries in {c.RED}sync.json{c.END}")
    sys.exit(1)
  mydict = INI.load("dict.ini")
  if not mydict:
    p.err(f"Missing or invalid {c.RED}dict.ini{c.END}")
    sys.exit(1)

  #---------------------------------------------------------------------------------- Resolve paths
  resolved = {}
  for name, paths in sync.items():
    resolved[name] = [replace_map(x, mydict, "{", "}") for x in paths]

  #------------------------------------------------------------------------------------- Validate
  errors = False
  for name, paths in resolved.items():
    seen = set()
    for path in paths:
      if not PATH.is_file(path):
        p.err(f"Path {c.ORANGE}{path}{c.END} in {c.RED}{name}{c.END} doesn't exist")
        errors = True
      if path in seen:
        p.err(f"Path {c.ORANGE}{path}{c.END} in {c.RED}{name}{c.END} duplicated")
        errors = True
      seen.add(path)
  if errors:
    sys.exit(1)

  if args.diff is None:
    p.wrn(f"Flag {c.GREY}-d{c.END} requires tag, e.g. {c.GREY}-d {c.MAGNTA}1.1{c.END}")
    args.diff = ""

  #----------------------------------------------------------------------------------------- Diff
  diff_ctx = {}
  if args.diff:
    diff_ctx["latest_nbr"], diff_ctx["obsolete_nbr"] = map(int, args.diff.split("."))

  #----------------------------------------------------------------------------------------- Sync
  update_flag = False
  nbr_last = 0

  def sync_file(name:str, paths:list[str]):
    nonlocal update_flag, nbr_last
    paths = [PATH.normalize(x) for x in paths]
    paths = [x for x in paths if PATH.is_file(x)]
    if len(paths) < 2: return
    hashs = [FILE.hash(f, algo="md5") for f in paths]
    stamps = [FILE.mtime(f) for f in paths]
    dts = [datetime.fromtimestamp(s).strftime("%Y-%m-%d %H:%M:%S") for s in stamps]
    if len(set(hashs)) == 1 and not args.info: return
    latest_id = stamps.index(max(stamps))
    latest_hash = hashs[latest_id]
    latest_file = paths[latest_id]
    latest_dt = dts[latest_id]
    nbr_last += 1
    nbr_obsolete = 0
    if diff_ctx and diff_ctx.get("latest_nbr") == nbr_last:
      diff_ctx["latest_file"] = latest_file
      diff_ctx["name"] = name
    p(f"{Ico.INF} {c.YELLOW}{nbr_last}{c.GREY}.x{c.END} Latest"
      f" {c.BLUE}{name}{c.END}: {c.GREY}{latest_file}{c.END}"
      f" {c.TEAL}{latest_dt}{c.END}")
    for file, hash, dt, stamp in zip(paths, hashs, dts, stamps):
      tag = lambda clr: f"{Ico.GAP} {clr}{nbr_last}.{nbr_obsolete}{c.END}"
      if hash != latest_hash:
        update_flag = True
        nbr_obsolete += 1
        color = c.YELLOW
        if(diff_ctx and diff_ctx.get("latest_nbr") == nbr_last
            and diff_ctx.get("obsolete_nbr") == nbr_obsolete):
          diff_ctx["obsolete_file"] = file
          color = c.GREEN
        if args.update:
          backed = utils.backup_file(file, name)
          try:
            DIR.copy(latest_file, file)
            msg = f"{c.GREY}{file}{c.END} updated"
            if backed: msg += f" {c.GREY}(backup){c.END}"
            msg += f" {c.GREEN}OK{c.END}"
            p(f"{tag(color)} {msg}")
          except Exception:
            p(f"{tag(color)} {c.GREY}{file}{c.END} update {c.RED}FAILED{c.END}")
        else:
          p(f"{tag(color)} Obsolete: {c.GREY}{file}{c.END} {c.ORANGE}{dt}{c.END}")
          if stamp == os.path.getctime(file):
            p.wrn("File was created recently, make sure it's not actually newer!")
      elif (args.update or args.info) and file != latest_file:
        p.ok(f"{c.GREY}{file}{c.END} is up-to-date")

  from . import utils

  for name, paths in resolved.items():
    sync_file(name, paths)

  if not update_flag:
    p.inf(f"All files are in the same version {c.GREY}(no update needed){c.END}")
  elif not args.update:
    p.run(f"Update older files using {c.YELLOW}-u{c.END} {c.GREY}--update{c.END}")
    p.run(f"Display file changes using {c.YELLOW}-d{c.END} {c.GREY}--diff{c.END}")
    if args.diff:
      if not diff_ctx or "obsolete_file" not in diff_ctx:
        p.err(f"Invalid tag {c.GREEN}{args.diff}{c.END} for comparing files")
        sys.exit(1)
      p.inf(f"Diff compare {c.BLUE}{diff_ctx['name']}{c.END}"
        f" tag {c.GREEN}{diff_ctx['latest_nbr']}.{diff_ctx['obsolete_nbr']}{c.END}:")
      reversed_dict = {PATH.normalize(v): f"{{{k}}}" for k, v in mydict.items()}
      from . import diff
      diff.show(diff_ctx["obsolete_file"], diff_ctx["latest_file"], reversed_dict)

if __name__ == "__main__":
  main()