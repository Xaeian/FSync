# fsync/args.py

import argparse

def load_args():
  parser = argparse.ArgumentParser(description="FSync: File synchronization tool")
  parser.add_argument("-w", "--workspace", type=str, nargs="?", const=".", default=None,
    help="Set workspace directory (default: current dir)")
  parser.add_argument("-u", "--update", action="store_true",
    help="Update files to latest version (most recently modified)")
  parser.add_argument("-i", "--info", action="store_true",
    help="Display all synchronized files")
  parser.add_argument("-e", "--example", action="store_true",
    help="Create example config files")
  parser.add_argument("-d", "--diff", type=str, nargs="?",
    help="Compare files by tag: <latest>.<obsolete>", default="")
  parser.add_argument("-v", "--version", action="store_true",
    help="Program version and repository")
  return parser.parse_args()