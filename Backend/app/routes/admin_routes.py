"""
Admin Routes: Administrative endpoints for managing songs and Dropbox sync.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.services.song_management_service import SongManagementService
from app.services.dropbox_sync_service import DropboxSyncService
import logging

router = APIRouter(prefix="/api/admin", tags=["admin"])
logger = logging.getLogger(__name__)


class DropboxSyncRequest(BaseModel):
    """Request model for Dropbox sync."""
    dropbox_folder_path: str
    operation: str = "sync"  # 'sync' or 'replace'


@router.post("/sync/dropbox")
def sync_dropbox_folder(request: DropboxSyncRequest):
    """
    Scan Dropbox folder and sync songs with database.

    Args:
        request: Contains path to local Dropbox folder

    Returns:
        Sync statistics and results

    Example:
        POST /api/admin/sync/dropbox
        {
            "dropbox_folder_path": "C:/Users/user/Dropbox/RagaRasa",
            "operation": "sync"
        }
    """
    try:
        # Validate path
        if not request.dropbox_folder_path:
            raise HTTPException(
                status_code=400,
                detail="dropbox_folder_path is required"
            )

        # Scan Dropbox folder
        songs_from_dropbox = DropboxSyncService.scan_local_dropbox_folder(
            request.dropbox_folder_path
        )

        if not songs_from_dropbox:
            raise HTTPException(
                status_code=400,
                detail="No songs found in Dropbox folder"
            )

        # Sync with database
        stats = SongManagementService.sync_songs_from_list(songs_from_dropbox)

        logger.info(f"Dropbox sync completed: {stats}")

        return {
            "status": "success",
            "message": "Dropbox folder synced successfully",
            "dropbox_folder": request.dropbox_folder_path,
            "operation": request.operation,
            "statistics": stats
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logger.error(f"Error syncing Dropbox folder: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/sync/status")
def get_sync_status():
    """
    Get status of sync services.

    Returns:
        Current sync service status
    """
    try:
        status = DropboxSyncService.get_sync_status()
        return {
            "status": "ok",
            "services": {
                "dropbox_sync": status
            }
        }
    except Exception as e:
        logger.error(f"Error getting sync status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/database/stats")
def get_database_stats():
    """
    Get statistics about songs in database.

    Returns:
        Database statistics (total songs, by rass, deleted, etc.)
    """
    try:
        from app.database import songs_collection

        # Get total active songs
        total_active = songs_collection.count_documents({"status": {"$ne": "deleted"}})
        
        # Get songs by rass
        rass_stats = {}
        for rass in ["shringar", "shaant", "veer", "shok"]:
            count = songs_collection.count_documents({
                "rass": rass,
                "status": {"$ne": "deleted"}
            })
            rass_stats[rass] = count

        # Get deleted songs count
        total_deleted = songs_collection.count_documents({"status": "deleted"})

        # Get total with all statuses
        total_all = songs_collection.count_documents({})

        return {
            "status": "ok",
            "statistics": {
                "total_active": total_active,
                "total_deleted": total_deleted,
                "total_all": total_all,
                "by_rass": rass_stats
            }
        }

    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/database/cleanup")
def cleanup_database(
    remove_deleted: bool = Query(False, description="Permanently remove all deleted songs")
):
    """
    Cleanup database.

    Args:
        remove_deleted: If True, permanently delete all soft-deleted songs

    Returns:
        Cleanup statistics
    """
    try:
        from app.database import songs_collection

        if remove_deleted:
            result = songs_collection.delete_many({"status": "deleted"})
            deleted_count = result.deleted_count
            
            logger.info(f"Cleaned up {deleted_count} deleted songs")

            return {
                "status": "success",
                "message": "Database cleaned up",
                "operations": {
                    "deleted_songs_removed": deleted_count
                }
            }
        else:
            # Just get count of what would be deleted
            deleted_count = songs_collection.count_documents({"status": "deleted"})

            return {
                "status": "success",
                "message": "Cleanup statistics",
                "preview": {
                    "songs_to_be_deleted": deleted_count
                }
            }

    except Exception as e:
        logger.error(f"Error cleaning up database: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/database/reset")
def reset_database_to_active():
    """
    Restore all soft-deleted songs (mark as active).
    Useful for recovering from accidental deletions.

    Returns:
        Recovery statistics
    """
    try:
        from app.database import songs_collection
        from datetime import datetime

        result = songs_collection.update_many(
            {"status": "deleted"},
            {
                "$set": {"status": "active", "updated_at": datetime.now().isoformat()},
                "$unset": {"deleted_at": ""}
            }
        )

        restored_count = result.modified_count

        logger.warning(f"Restored {restored_count} deleted songs")

        return {
            "status": "success",
            "message": "All deleted songs restored to active",
            "songs_restored": restored_count
        }

    except Exception as e:
        logger.error(f"Error restoring deleted songs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
