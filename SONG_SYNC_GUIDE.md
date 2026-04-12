# Song Database Synchronization System

## Overview

The RagaRasa Music Therapy application now includes an automated database synchronization system that keeps the MongoDB database in sync with songs in the Dropbox folder. The system supports three main operations:

1. **Add Songs** - New songs are automatically created in the database
2. **Update Songs** - Modified song information is updated in the database
3. **Delete Songs** - Removed songs are marked as deleted (soft delete)

## Features

### Automatic Sync
- Scan Dropbox folder for audio files (MP3, WAV, FLAC, M4A, AAC, OGG)
- Automatically create/update database records
- Track metadata (created_at, updated_at, status)

### Soft Delete
- Songs are soft-deleted by default (marked with `status: "deleted"`)
- Allows recovery of accidentally deleted songs
- Can be restored anytime

### Manual Sync Options
- **API Endpoints** - RESTful API for programmatic sync
- **Python Script** - Command-line tool for manual sync
- **Admin Dashboard** - Database statistics and management

## Database Schema

Each song document in MongoDB has the following structure:

```json
{
  "_id": "ObjectId",
  "song_name": "Song_Name.mp3",
  "rass": "shaant",  // shringar, shaant, veer, shok
  "file_path": "/path/to/song.mp3",
  "dropbox_path": "/Shaant/Song_Name.mp3",
  "dropbox_url": "https://...",
  "features": [],
  "confidence": 0.5,
  "ratings": {
    "avg_rating": 0,
    "num_users": 0
  },
  "metadata": {
    "source": "dropbox",
    "format": "MP3",
    "last_scanned": "2026-04-12T..."
  },
  "created_at": "2026-04-12T...",
  "updated_at": "2026-04-12T...",
  "status": "active"  // active, deleted
}
```

## API Endpoints

### Song Management

#### Create Song
```bash
POST /api/songs/create
Content-Type: application/json

{
  "song_name": "New_Song.mp3",
  "rass": "shaant",
  "file_path": "/path/to/song.mp3",
  "dropbox_path": "/Shaant/New_Song.mp3",
  "dropbox_url": "https://..."
}
```

#### Update Song
```bash
PUT /api/songs/{song_id}
Content-Type: application/json

{
  "dropbox_url": "https://new-url",
  "metadata": {...}
}
```

#### Delete Song (Soft Delete)
```bash
DELETE /api/songs/{song_id}
```

#### Delete Song (Permanent)
```bash
DELETE /api/songs/{song_id}?hard=true
```

#### Restore Deleted Song
```bash
POST /api/songs/{song_id}/restore
```

### Admin Operations

#### Sync Dropbox Folder
Scan local Dropbox folder and update database:

```bash
POST /api/admin/sync/dropbox
Content-Type: application/json

{
  "dropbox_folder_path": "C:/Users/user/Dropbox/RagaRasa",
  "operation": "sync"
}
```

#### Get Database Statistics
```bash
GET /api/admin/database/stats
```

Response:
```json
{
  "status": "ok",
  "statistics": {
    "total_active": 65,
    "total_deleted": 3,
    "total_all": 68,
    "by_rass": {
      "shringar": 7,
      "shaant": 30,
      "veer": 8,
      "shok": 20
    }
  }
}
```

#### Get Deleted Songs
```bash
GET /api/songs/admin/deleted
```

#### Cleanup Database
Remove all soft-deleted songs permanently:

```bash
POST /api/admin/database/cleanup?remove_deleted=true
```

#### Restore All Deleted Songs
```bash
POST /api/admin/database/reset
```

## Command-Line Tool

### Installation

The sync script is located at: `Backend/scripts/sync_dropbox_songs.py`

### Usage

```bash
# Basic sync
python sync_dropbox_songs.py --path "C:/Users/user/Dropbox/RagaRasa"

# Preview changes without applying
python sync_dropbox_songs.py --path "C:/Users/user/Dropbox/RagaRasa" --dry-run

# List all songs found
python sync_dropbox_songs.py --path "C:/Users/user/Dropbox/RagaRasa" --list-songs

# Sync and show database statistics
python sync_dropbox_songs.py --path "C:/Users/user/Dropbox/RagaRasa" --show-stats
```

### Examples

```bash
# Scan and sync Dropbox folder
cd C:\Users\rishi\OneDrive\Desktop\Raga Rasa Laya\Backend
python scripts/sync_dropbox_songs.py --path "C:\Users\rishi\Dropbox\RagaRasa"

# Preview what would be synced
python scripts/sync_dropbox_songs.py --path "C:\Users\rishi\Dropbox\RagaRasa" --dry-run

# Sync and show statistics
python scripts/sync_dropbox_songs.py --path "C:\Users\rishi\Dropbox\RagaRasa" --show-stats
```

## Folder Structure

Expected Dropbox folder structure:

```
RagaRasa/
├── Shringar/
│   ├── Song1.mp3
│   ├── Song2.mp3
│   └── ...
├── Shaant/
│   ├── Song1.mp3
│   ├── Song2.mp3
│   └── ...
├── Veer/
│   ├── Song1.mp3
│   └── ...
└── Shok/
    ├── Song1.mp3
    └── ...
```

Each rass subfolder contains the audio files for that rass.

## Supported Audio Formats

- MP3 (`.mp3`)
- WAV (`.wav`)
- FLAC (`.flac`)
- M4A (`.m4a`)
- AAC (`.aac`)
- OGG (`.ogg`)

## How It Works

### Adding a Song
1. Place a new audio file in the Dropbox folder under the appropriate rass subfolder
2. Run sync command or API endpoint
3. System scans the folder and finds the new file
4. Creates a new document in MongoDB with metadata
5. Generates Dropbox streaming URL

### Updating a Song
1. Modify the audio file or its location in Dropbox
2. Run sync command or API endpoint
3. System finds the existing song by name
4. Updates the document with new metadata
5. Updates timestamps

### Deleting a Song
1. Remove the audio file from Dropbox folder
2. Run sync command or API endpoint
3. System detects the missing file
4. Marks song as deleted (soft delete)
5. Can be restored later if needed

## Best Practices

### For Manual Sync
1. **Always dry-run first**: Use `--dry-run` to preview changes
2. **Check statistics**: Use `--show-stats` to verify database state
3. **Backup before sync**: Keep backups of MongoDB data
4. **Schedule regular syncs**: Run sync after adding/removing songs

### For Production
1. Set up scheduled sync jobs (e.g., daily)
2. Monitor sync logs for errors
3. Use soft delete for data safety
4. Regularly clean up deleted songs (if needed)
5. Keep Dropbox folder well-organized

## Troubleshooting

### No songs found
- Verify Dropbox folder path is correct
- Check folder contains rass subfolders (Shringar, Shaant, Veer, Shok)
- Ensure audio files have supported extensions

### Sync errors
- Check MongoDB connection
- Verify Dropbox folder is accessible
- Check file permissions
- See logs for detailed error messages

### Database sync failed
- Verify MongoDB is running
- Check connection string in `app/config.py`
- Ensure database has correct permissions
- Try smaller batch of songs first

## Services

### SongManagementService
Located in: `app/services/song_management_service.py`

Handles:
- Creating songs
- Updating songs
- Deleting songs (soft/hard)
- Restoring deleted songs
- Bulk sync operations

### DropboxSyncService
Located in: `app/services/dropbox_sync_service.py`

Handles:
- Scanning local Dropbox folder
- Building song documents from files
- Generating Dropbox URLs
- Tracking metadata

## Future Enhancements

1. **Real-time Sync**: Use file watchers to detect changes automatically
2. **Dropbox API Integration**: Direct integration with Dropbox API
3. **Web Admin Dashboard**: UI for managing songs
4. **Auto-cleanup**: Automated deletion of old versions
5. **Backup & Restore**: Full database backup/restore functionality
6. **Audit Logging**: Track all changes with timestamps
7. **Notifications**: Alerts for sync failures
8. **Batch Operations**: Process multiple songs at once

## Files

- `app/services/song_management_service.py` - CRUD operations
- `app/services/dropbox_sync_service.py` - Dropbox folder scanning
- `app/routes/song_management_routes.py` - Song CRUD API endpoints
- `app/routes/admin_routes.py` - Admin/sync API endpoints
- `scripts/sync_dropbox_songs.py` - Command-line sync tool
- `app/config.py` - Configuration settings
