#!/usr/bin/env python3
"""
sync_dropbox_songs.py: Standalone script to sync songs from Dropbox folder to MongoDB.

Usage:
    python sync_dropbox_songs.py --path "C:/Users/user/Dropbox/RagaRasa"
    python sync_dropbox_songs.py --path "C:/Users/user/Dropbox/RagaRasa" --show-stats
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.dropbox_sync_service import DropboxSyncService
from app.services.song_management_service import SongManagementService


def print_header(text):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_stats(stats):
    """Print sync statistics."""
    print(f"Created:  {stats['created']}")
    print(f"Updated:  {stats['updated']}")
    print(f"Deleted:  {stats['deleted']}")

    if stats['errors']:
        print(f"\nErrors ({len(stats['errors'])}):")
        for error in stats['errors']:
            print(f"  - {error['song']}: {error['error']}")


def main():
    parser = argparse.ArgumentParser(
        description="Sync songs from Dropbox folder to MongoDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sync_dropbox_songs.py --path "C:/Users/user/Dropbox/RagaRasa"
  python sync_dropbox_songs.py --path "C:/Users/user/Dropbox/RagaRasa" --show-stats
  python sync_dropbox_songs.py --path "C:/Users/user/Dropbox/RagaRasa" --list-songs
        """
    )

    parser.add_argument(
        "--path",
        required=True,
        help="Path to local Dropbox folder (e.g., C:/Users/user/Dropbox/RagaRasa)"
    )
    parser.add_argument(
        "--show-stats",
        action="store_true",
        help="Show database statistics after sync"
    )
    parser.add_argument(
        "--list-songs",
        action="store_true",
        help="List all songs found (preview before syncing)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without updating database"
    )

    args = parser.parse_args()

    print_header("Raga-Rasa Dropbox Song Sync")

    # Validate path
    dropbox_path = Path(args.path)
    if not dropbox_path.exists():
        print(f"ERROR: Dropbox folder not found: {args.path}")
        sys.exit(1)

    print(f"Dropbox folder: {args.path}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        # Scan Dropbox folder
        print("Scanning Dropbox folder for audio files...")
        songs = DropboxSyncService.scan_local_dropbox_folder(str(dropbox_path))

        print(f"Found {len(songs)} songs\n")

        if not songs:
            print("No songs found in Dropbox folder!")
            sys.exit(0)

        # Show songs if requested
        if args.list_songs:
            print_header("Songs Found")
            for i, song in enumerate(songs, 1):
                print(f"{i}. {song['song_name']}")
                print(f"   Rass: {song['rass']}")
                print(f"   Path: {song['dropbox_path']}\n")

        # Dry run - just show what would happen
        if args.dry_run:
            print_header("Dry Run - Preview Changes")
            print(f"Would create/update {len(songs)} songs")
            return

        # Sync with database
        print_header("Syncing with Database")
        print("Updating MongoDB...")

        stats = SongManagementService.sync_songs_from_list(songs)

        print("\nSync completed!\n")
        print_stats(stats)

        # Show database stats if requested
        if args.show_stats:
            print_header("Database Statistics")
            from app.database import songs_collection

            total_active = songs_collection.count_documents({"status": {"$ne": "deleted"}})
            total_deleted = songs_collection.count_documents({"status": "deleted"})

            print(f"Total active songs: {total_active}")
            print(f"Total deleted songs: {total_deleted}")

            print("\nSongs by Rass:")
            for rass in ["shringar", "shaant", "veer", "shok"]:
                count = songs_collection.count_documents({
                    "rass": rass,
                    "status": {"$ne": "deleted"}
                })
                print(f"  {rass.capitalize()}: {count}")

        print_header("Sync Complete")
        print("Database is now synchronized with Dropbox folder!\n")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
