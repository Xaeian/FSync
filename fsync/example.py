# fsync/example.py

"""Generate example config files (dict.ini, sync.json)."""

import os, platform
from xaeian import JSON, INI, FILE, Print
from xaeian.colors import Color as c

def create():
  p = Print()
  user = os.getlogin()
  if platform.system() == "Windows": base = f"C:/Users/{user}"
  else: base = f"/home/{user}"
  mydict = {
    "web": f"{base}/Projects/WebPage/backend",
    "staff": f"{base}/Desktop/MyStaff/test",
    "work": f"{base}/Work/Drivers/repos",
  }
  sync = {
    "serial.c": ["{staff}/serial.c", "{work}/PLC/serial_port.c"],
    "utils.py": ["{web}/lib/utils.py", "{work}/PLC/misc.py"],
  }
  for name, data, saver in [
    ("dict.ini", mydict, INI.save),
    ("sync.json", sync, JSON.save_pretty),
  ]:
    if FILE.exists(name):
      p.err(f"File {c.RED}{name}{c.END} already exists. Delete it to generate example")
    else:
      saver(name, data)
      p.ok(f"Template {c.GREEN}{name}{c.END} generated")