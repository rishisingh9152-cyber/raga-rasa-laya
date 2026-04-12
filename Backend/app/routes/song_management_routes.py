"""
Song Management Routes: API endpoints for CRUD operations on songs.
Handles adding, updating, and deleting songs with database synchronization.
"""

from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.services.song_management_service import SongManagementService
import logging

router = APIRouter(prefix="/api/songs", tags=["songs"])
logger = logging.getLogger(__name__)


# ========================
# PYDANTIC MODELS
# ========================
class SongCreate(BaseModel):
    """Model for creating a new song."""
    song_name: str = Field(..., min_length=1, description="Song name")
    rass: str = Field(..., description="Rasa type: shringar, shaant, veer, shok")
    file_path: str = Field(..., description="Local file path")
    dropbox_path: Optional[str] = Field(None, description="Path in Dropbox")
    dropbox_url: Optional[str] = Field(None, description="Dropbox streaming URL")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class SongUpdate(BaseModel):
    """Model for updating a song."""
    song_name: Optional[str] = None
    rass: Optional[str] = None
    file_path: Optional[str] = None
    dropbox_path: Optional[str] = None
    dropbox_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BulkSyncRequest(BaseModel):
    """Model for bulk syncing songs from Dropbox."""
    songs: List[Dict[str, Any]] = Field(..., description="List of songs to sync")
    operation: str = Field("sync", description="Operation type: sync, replace")


# ========================
# CREATE SONG
# ========================
@router.post("/create")
def create_song(song_data: SongCreate):
    """
    Create a new song in the database.

    Args:
        song_data: Song creation data

    Returns:
        Created song document
    """
    try:
        created_song = SongManagementService.create_song(
            song_name=song_data.song_name,
            rass=song_data.rass,
            file_path=song_data.file_path,
            dropbox_path=song_data.dropbox_path,
            dropbox_url=song_data.dropbox_url,
            metadata=song_data.metadata
        )

        return {
            "status": "success",
            "message": f"Song created: {song_data.song_name}",
            "data": created_song
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.error(f"Error creating song: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ========================
# UPDATE SONG
# ========================
@router.put("/{song_id}")
def update_song(song_id: str, updates: SongUpdate):
    """
    Update an existing song.

    Args:
        song_id: MongoDB song ID (24-character hex string)
        updates: Fields to update

    Returns:
        Updated song document
    """
    try:
        update_dict = updates.dict(exclude_unset=True)

        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")

        updated_song = SongManagementService.update_song(song_id, update_dict)

        if not updated_song:
            raise HTTPException(status_code=404, detail=f"Song not found: {song_id}")

        return {
            "status": "success",
            "message": f"Song updated: {song_id}",
            "data": updated_song
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        logger.error(f"Error updating song: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ========================
# DELETE SONG (SOFT)
# ========================
@router.delete("/{song_id}")
def delete_song(song_id: str, hard: bool = Query(False, description="Permanently delete")):
    """
    Delete a song (soft delete by default).

    Args:
        song_id: MongoDB song ID
        hard: If True, permanently delete. If False, soft delete (mark as inactive)

    Returns:
        Success message
    """
    try:
        if hard:
            deleted = SongManagementService.hard_delete_song(song_id)
            message = "Song permanently deleted"
        else:
            deleted = SongManagementService.delete_song(song_id)
            message = "Song marked as deleted"

        if not deleted:
            raise HTTPException(status_code=404, detail=f"Song not found: {song_id}")

        return {
            "status": "success",
            "message": message,
            "song_id": song_id
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        logger.error(f"Error deleting song: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ========================
# RESTORE SONG
# ========================
@router.post("/{song_id}/restore")
def restore_song(song_id: str):
    """
    Restore a soft-deleted song.

    Args:
        song_id: MongoDB song ID of deleted song

    Returns:
        Restored song document
    """
    try:
        restored_song = SongManagementService.restore_song(song_id)

        if not restored_song:
            raise HTTPException(status_code=404, detail=f"Song not found: {song_id}")

        return {
            "status": "success",
            "message": f"Song restored: {song_id}",
            "data": restored_song
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        logger.error(f"Error restoring song: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ========================
# BULK SYNC (FROM DROPBOX)
# ========================
@router.post("/admin/sync")
def sync_songs(request: BulkSyncRequest):
    """
    Bulk sync songs from Dropbox folder.
    This endpoint synchronizes the database with songs from Dropbox.

    Args:
        request: BulkSyncRequest with list of songs

    Returns:
        Sync statistics (created, updated, deleted)

    Example:
        POST /api/songs/admin/sync
        {
            "songs": [
                {
                    "song_name": "Song1.mp3",
                    "rass": "shaant",
                    "file_path": "/path/to/song1.mp3",
                    "dropbox_path": "/Shaant/Song1.mp3",
                    "dropbox_url": "https://..."
                },
                ...
            ],
            "operation": "sync"
        }

    Returns:
        {
            "status": "success",
            "statistics": {
                "created": 10,
                "updated": 5,
                "deleted": 2,
                "errors": []
            }
        }
    """
    try:
        if not request.songs:
            raise HTTPException(status_code=400, detail="Songs list cannot be empty")

        stats = SongManagementService.sync_songs_from_list(request.songs)

        return {
            "status": "success",
            "message": f"Sync completed successfully",
            "operation": request.operation,
            "statistics": stats
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        logger.error(f"Error syncing songs: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ========================
# GET DELETED SONGS
# ========================
@router.get("/admin/deleted")
def get_deleted_songs():
    """
    Get all soft-deleted songs (for recovery).

    Returns:
        List of deleted songs
    """
    try:
        deleted_songs = SongManagementService.get_deleted_songs()

        return {
            "status": "success",
            "count": len(deleted_songs),
            "songs": deleted_songs
        }

    except Exception as e:
        logger.error(f"Error fetching deleted songs: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
