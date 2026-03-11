# fsync/diff.py

__extras__ = ("diff", ["rich"])

import sys, difflib
from xaeian import FILE, PATH, Print, Color as c, replace_map

def show(file_a:str, file_b:str, mapping:dict|None=None):
  try:
    from rich.console import Console
    from rich.syntax import Syntax
  except ImportError:
    p = Print()
    p.err(f"Missing {c.TURQUS}rich{c.END} package for diff display")
    p.run(f"Install: {c.YELLOW}pip{c.END} install fsync[diff]")
    sys.exit(1)
  lines_a = FILE.load_lines(file_a)
  lines_b = FILE.load_lines(file_b)
  if mapping:
    label_a = replace_map(PATH.normalize(file_a), mapping)
    label_b = replace_map(PATH.normalize(file_b), mapping)
  else:
    label_a, label_b = file_a, file_b
  result = "".join(difflib.unified_diff(
    lines_a, lines_b,
    fromfile=label_a, tofile=label_b,
  ))
  if result:
    Console().print(Syntax(
      result, "diff", theme="ansi_dark",
      line_numbers=True, background_color=None,
    ))