## 📖 FSync

This tool **eliminates the problem of scattered libraries** by synchronizing 🔄 selected files spread across different projects on your machine _(locally)_. No more chaos and manual file copying.

At first glance, centralizing libraries seems like a great idea. It makes work easier and avoids code duplication. In practice, however, some complications arise:

- You don't always want to update a library in a project you're no longer developing, but it still needs to work.
- Some libraries must be part of the repository. When you hand off/close a project, you want everything in one place, without having to pull additional dependencies from external sources.
- It's better when all resources are in the project directory. It simplifies configuration _(Makefile, CMake)_, eliminates path and version issues, and improves IDE integration.

This solution is perfect if you run many smaller projects and care about efficient library management _(code that appears across multiple projects)_. If you make frequent changes, want to avoid messy code, but don't have time to spend hours organizing dependencies — this tool is for you! The program is dead simple. What matters is efficient and effective work, without unnecessary bureaucracy. The open source community can do its thing, but here the priority is a happy client and a working project done ⚡**fast** and 👍**good enough**.

### 🧐 Problems!

- ❌ **Possible accidental overwrites**: if you edit two versions of a library at the same time.
- ✅ Avoid this, but if it happens, every overwritten version is saved as a timestamped backup, so you can always recover your changes.
- ❌ **No environment isolation**: different projects may require different versions of the same library.
- ✅ Not a problem! Just create separate entries for different versions, keeping synchronization independent. You can also comment out entries for libraries that shouldn't be updated anymore.
- ❌ **Code duplication across repositories**: instead of one library copy, you have several in different projects.
- ✅ That's the point! Each client should have their own library version, with no dependencies on other repos. Full control, zero unnecessary complications.

### 🤔 Alternatives?

Of course you can approach this more professionally by:

- Versioning libraries as separate projects/repositories and updating them as needed.
- Using Git **Submodules**, which allows tracking library versions in the repository.
- External package managers _(`pip`, `npm`, `cargo`)_ that simplify dependency management.

If any of our libraries reach a stable version that we don't chaotically change every project, and they're good enough, it's worth considering one of the above solutions.

### ⚙️ Config

The **`sync.json`** file defines file synchronization configuration. Each entry is a key _(filename)_ and a list of paths to synchronize. Keys starting with `#` are treated as commented out and skipped.

Paths can use shorthand notation via the **`dict.ini`** file, which defines aliases for frequently repeated locations. In `sync.json` paths you can reference these aliases using `{key}` notation.

#### Example

Running the program with the `-e`, `--example` flag will create example config files locally.

File `dict.ini`
```ini
web = C:/Users/Me/Projects/WebPage/backend
staff = C:/Users/Me/Desktop/MyStaff/test
work = C:/Users/Me/Work/Drivers/repos
```

File `sync.json`
```json
{
  "serial.c": ["{staff}/serial.c", "{work}/PLC/serial_port.c"],
  "utils.py": ["{web}/lib/utils.py", "{work}/PLC/misc.py"],
  "#old_lib.c": ["{staff}/old_lib.c", "{work}/legacy/old_lib.c"]
}
```

### 🚀 Use

First, set the workspace — the directory containing your config files (`sync.json`, `dict.ini`) and where backups will be stored:
```bash
py -m fsync -w C:/Projects/sync  # specified path
py -m fsync -w                   # current directory
```

Running the program generates a report:
```bash
py -m fsync
```

To synchronize _(i.e. update older file versions)_, just add the `-u`, `--update` flag:
```bash
py -m fsync -u
```

For each pair of files with discrepancies, tags are generated. You can use them to inspect differences between files with the `-d`, `--diff` flag:
```bash
py -m fsync -d 1.1
```