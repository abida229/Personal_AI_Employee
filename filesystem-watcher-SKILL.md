---
name: filesystem-watcher
description: |
  Monitor file system for new files and create action items. 
  Watches a designated drop folder and creates corresponding action items in the vault.
---

# File System Watcher Skill

Automates monitoring of file system events and creates action items when files are added to a designated drop folder.

## Functionality

### Start File Watcher
```bash
python filesystem_watcher.py
```

### Stop File Watcher
Press `Ctrl+C` to stop the watcher process.

## Workflow

1. Place files in the `Drop_Folder` directory
2. The watcher detects the new file
3. Creates a metadata file in `Needs_Action` folder
4. Copies the original file to `Inbox` folder
5. The AI Employee can then process the action item

## Configuration

- **Drop Folder:** `./Drop_Folder/` (monitored location)
- **Target Folder:** Files are copied to `./Inbox/`
- **Action Items:** Created in `./Needs_Action/` with metadata

## Supported File Types

- `.txt`, `.pdf`, `.docx`, `.jpg`, `.png`, `.md`
- Additional types can be added by modifying the extension list in the script

## Monitoring

The watcher logs activities to `logs/filesystem_watcher.log` and provides real-time output to the console.