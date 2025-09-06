# mcclear
A simple, powerful tool to clear temporary cache files and folders from Minecraft servers, allowing them to be distributed as smaller, cleaner zip files.
(Though, this tool can also be used for any other folder type, as you can define your own deletion template)

## Why use mcclear?
When sharing or backing up a Minecraft server, folders like `logs`, `cache`, and plugin-specific data can take up a huge amount of space. `mcclear` uses customizable templates to intelligently purge these unnecessary files, dramatically reducing the server's file size without affecting the core world data or configurations you need.

## Features
- **Template-Based Cleaning:** Define simple `.txt` templates to specify which files and folders to delete.
- **Wildcard Support:** Use powerful wildcards (`*`, `**`) to match patterns, like deleting the `libs` folder from every plugin.
- **Detailed Stats:** Get a clear summary of the cleanup, showing how many files were deleted and how much space was saved.
- **No Dependencies:** Runs with a standard Python 3 installation. No `pip` installs required!

## Prerequisites
- [Python 3.6+](https://www.python.org/)

## Installation & Setup
1. Clone this repository or download the files as a ZIP.
2. **IMPORTANT:** Customize the `templates/default.txt` file or add your own new templates (e.g., `bungeecord.txt`).
	1. The default template may delete items you want to keep, so check each line to make sure it only contains cache data for the server or your plugins. Your plugins will probably be different to the default, so you may need to go in and add more plugin /lib folders.

## How to Use
1. Run the main script:
    - From your terminal: `python main.py`
    - On Windows, you can simply double-click the `main.py` file.
2. When prompted, enter the full path to the Minecraft server folder you want to clean.
3. When prompted, enter the name of the template you wish to use (e.g., `default`).
4. The script will perform the purge and show you a final summary. The window will stay open until you press Enter.

## Creating Templates
Templates are simple `.txt` files located in the `templates/` directory. Each line represents a file or folder pattern to be deleted.
- **Folders:** Start with a `/`. The folder and all its contents will be deleted.
- **Files:** You can use wildcards to match file names or types.
- **Wildcards:** The `*` character can be used to match any string of characters within a folder name or filename.
- **Comments:** Lines starting with `#` are ignored.
### Example Template
```
# Server Logs and Caches
/logs
/cache

# Plugin Data
# Deletes the 'libs' and 'lib' folder inside any plugin directory
/plugins/*/libs
/plugins/*/lib

# Specific plugin files
/plugins/AxVaults/data.db

# Root directory files
# Deletes all .json files in the main server folder
/*.json
```
This template would delete:
- The entire `/logs/` directory.
- The entire `/cache/` directory.
- The `libs` and `lib` folder inside `/plugins/AxRewards/`, `/plugins/AxVaults/`, etc.
- The specific `data.db` file for the `AxVaults` plugin.
- `usercache.json`, `banned-players.json`, etc., from the server's root directory.