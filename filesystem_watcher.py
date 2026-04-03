"""
File System Watcher for AI Employee
Monitors a designated drop folder and creates action items when files are added.
"""
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from datetime import datetime


class DropFolderHandler(FileSystemEventHandler):
    """Handles file system events in the drop folder."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'

        # Create directories if they don't exist
        self.needs_action.mkdir(exist_ok=True)
        self.inbox.mkdir(exist_ok=True)

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        source = Path(event.src_path)
        if source.suffix.lower() in ['.txt', '.pdf', '.docx', '.jpg', '.png', '.md']:
            self.process_new_file(source)

    def on_moved(self, event):
        """Handle file move events."""
        if event.is_directory:
            return

        dest = Path(event.dest_path)
        if dest.suffix.lower() in ['.txt', '.pdf', '.docx', '.jpg', '.png', '.md']:
            self.process_new_file(dest)

    def process_new_file(self, source: Path):
        """Process a new file by creating a corresponding action item."""
        # Wait briefly to ensure file is fully written
        time.sleep(0.5)

        # Copy file to inbox
        dest_file = self.inbox / f'FILE_{source.name}'
        if not dest_file.exists():
            # Retry copy in case file is still being written
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    shutil.copy2(source, dest_file)
                    break
                except (PermissionError, FileNotFoundError) as e:
                    if attempt < max_retries - 1:
                        time.sleep(0.5)
                    else:
                        self.logger.error(f"Failed to copy {source.name}: {e}")
                        return

        # Create metadata file
        meta_path = self.needs_action / f'FILE_ACTION_{source.stem}_{int(time.time())}.md'

        file_size = source.stat().st_size
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        meta_content = f"""---
type: file_drop
original_name: {source.name}
size: {file_size} bytes
priority: medium
status: pending
created: {timestamp}
---

# New File Received

## File Information
- **Original Name:** {source.name}
- **Size:** {file_size} bytes
- **Location:** {source.parent}
- **Received:** {timestamp}

## Content Preview
{self.get_file_preview(source)}

## Suggested Actions
- [ ] Review file content
- [ ] Determine appropriate response
- [ ] Take required action
- [ ] Move to Done when complete

## Notes
"""
        meta_path.write_text(meta_content)
        print(f"Created action item for: {source.name}")


    def get_file_preview(self, source: Path):
        """Get a preview of the file content based on file type."""
        try:
            if source.suffix.lower() in ['.txt', '.md']:
                # Read first 500 characters of text files
                with open(source, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(500)
                    return content.strip() + ("..." if len(content) >= 500 else "")
            elif source.suffix.lower() in ['.pdf']:
                return "[PDF File - please review manually]"
            elif source.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                return "[Image File - please review manually]"
            else:
                return f"[{source.suffix.upper()} File - please review manually]"
        except Exception:
            return "[Unable to read file content]"


def main():
    """Main function to run the file system watcher."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/filesystem_watcher.log'),
            logging.StreamHandler()
        ]
    )

    vault_path = Path.cwd()  # Current directory as vault
    drop_folder = vault_path / 'Drop_Folder'  # Folder to watch
    drop_folder.mkdir(exist_ok=True)  # Create if it doesn't exist

    event_handler = DropFolderHandler(vault_path)
    observer = Observer()
    observer.schedule(event_handler, str(drop_folder), recursive=False)

    print(f"File System Watcher started. Monitoring: {drop_folder}")
    print(f"Files placed in {drop_folder} will be processed.")
    print("Press Ctrl+C to stop.")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping File System Watcher...")

    observer.join()


if __name__ == "__main__":
    main()