# AI Employee Launcher

This directory contains the complete Bronze Tier implementation for the Personal AI Employee project.

## Directory Structure
```
├── Dashboard.md              # Main dashboard with metrics
├── Company_Handbook.md       # Rules of engagement
├── filesystem_watcher.py     # File system monitoring script
├── requirements.txt          # Python dependencies
├── test_claude_write.md      # Demonstration of read/write capability
├── filesystem-watcher-SKILL.md # Skill definition
├── BRONZE_TIER_COMPLETE.md   # Completion guide
├── Inbox/                    # Incoming items
├── Needs_Action/             # Items requiring attention
├── Done/                     # Completed items
├── Plans/                    # Planning documents
├── Pending_Approval/         # Items awaiting approval
├── Approved/                 # Approved items
├── Rejected/                 # Rejected items
├── Logs/                     # Log files
└── Drop_Folder/              # Watched folder for new files
```

## Running the System

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Start the file watcher:
   ```
   python filesystem_watcher.py
   ```

3. Place files in the Drop_Folder to trigger actions.

## Bronze Tier Requirements Met

✅ Obsidian vault with Dashboard.md and Company_Handbook.md
✅ One working Watcher script (File system monitoring)
✅ Claude Code successfully reading from and writing to the vault
✅ Basic folder structure: /Inbox, /Needs_Action, /Done
✅ All AI functionality implemented as Agent Skills