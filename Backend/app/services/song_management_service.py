"""
SongManagementService: Manages song CRUD operations with database synchronization.
Handles adding, updating, and deleting songs with proper tracking.
"""

from typing import Optional, Dict, Any, List
from app.database import songs_collection
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SongManagementService:
    """Service for managing songs in the database."""

    @staticmethod
    def create_song(
        song_name: str,
        rass: str,
        file_path: str,
        dropbox_path: Optional[str] = None,
        dropbox_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new song in the database.

        Args:
            song_name: Name of the song
            rass: Rasa type (shringar, shaant, veer, shok)
            file_path: Local file path
            dropbox_path: Path in Dropbox
            dropbox_url: Dropbox streaming URL
            metadata: Additional metadata (artist, duration, etc.)

        Returns:
            Created song document with _id

        Raises:
            ValueError: If song already exists or invalid data
        """
        try:
            # Validate rass
            valid_rasses = ["shringar", "shaant", "veer", "shok"]
            if rass.lower() not in valid_rasses:
                raise ValueError(f"Invalid rass. Must be one of: {valid_rasses}")

            # Check if song already exists
            existing = songs_collection.find_one({"song_name": song_name})
            if existing:
                raise ValueError(f"Song already exists: {song_name}")

            song_doc = {
                "song_name": song_name,
                "rass": rass.lower(),
                "file_path": file_path,
                "dropbox_path": dropbox_path or "",
                "dropbox_url": dropbox_url or "",
                "features": [],
                "confidence": 0.5,
                "ratings": {
                    "avg_rating": 0,
                    "num_users": 0
                },
                "metadata": metadata or {},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "active"
            }

            result = songs_collection.insert_one(song_doc)
            song_doc["_id"] = str(result.inserted_id)

            logger.info(f"Song created: {song_name} ({result.inserted_id})")
            return song_doc

        except ValueError as ve:
            logger.error(f"Validation error creating song {song_name}: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error creating song {song_name}: {e}")
            raise

    @staticmethod
    def update_song(
        song_id: str,
        updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update an existing song.

        Args:
            song_id: MongoDB song ID
            updates: Dictionary of fields to update

        Returns:
            Updated song document or None if not found

        Raises:
            ValueError: If song_id is invalid
        """
        try:
            song_obj_id = ObjectId(song_id)
        except Exception as e:
            logger.error(f"Invalid song_id format: {song_id}")
            raise ValueError(f"Invalid song_id format: {song_id}")

        try:
            # Validate rass if being updated
            if "rass" in updates:
                valid_rasses = ["shringar", "shaant", "veer", "shok"]
                if updates["rass"].lower() not in valid_rasses:
                    raise ValueError(f"Invalid rass. Must be one of: {valid_rasses}")
                updates["rass"] = updates["rass"].lower()

            # Add timestamp
            updates["updated_at"] = datetime.now().isoformat()

            # Update document
            result = songs_collection.find_one_and_update(
                {"_id": song_obj_id},
                {"$set": updates},
                return_document=True
            )

            if result:
                result["_id"] = str(result["_id"])
                logger.info(f"Song updated: {song_id}")
            else:
                logger.warning(f"Song not found for update: {song_id}")

            return result

        except ValueError as ve:
            logger.error(f"Validation error updating song {song_id}: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error updating song {song_id}: {e}")
            raise

    @staticmethod
    def delete_song(song_id: str) -> bool:
        """
        Delete a song (soft delete - mark as inactive).

        Args:
            song_id: MongoDB song ID

        Returns:
            True if deleted, False if not found

        Raises:
            ValueError: If song_id is invalid
        """
        try:
            song_obj_id = ObjectId(song_id)
        except Exception as e:
            logger.error(f"Invalid song_id format: {song_id}")
            raise ValueError(f"Invalid song_id format: {song_id}")

        try:
            # Soft delete - mark as inactive
            result = songs_collection.update_one(
                {"_id": song_obj_id},
                {
                    "$set": {
                        "status": "deleted",
                        "deleted_at": datetime.now().isoformat()
                    }
                }
            )

            if result.matched_count > 0:
                logger.info(f"Song deleted (soft): {song_id}")
                return True
            else:
                logger.warning(f"Song not found for deletion: {song_id}")
                return False

        except Exception as e:
            logger.error(f"Error deleting song {song_id}: {e}")
            raise

    @staticmethod
    def hard_delete_song(song_id: str) -> bool:
        """
        Permanently delete a song from database.

        Args:
            song_id: MongoDB song ID

        Returns:
            True if deleted, False if not found
        """
        try:
            song_obj_id = ObjectId(song_id)
        except Exception as e:
            logger.error(f"Invalid song_id format: {song_id}")
            raise ValueError(f"Invalid song_id format: {song_id}")

        try:
            result = songs_collection.delete_one({"_id": song_obj_id})

            if result.deleted_count > 0:
                logger.warning(f"Song permanently deleted: {song_id}")
                return True
            else:
                logger.warning(f"Song not found for hard deletion: {song_id}")
                return False

        except Exception as e:
            logger.error(f"Error hard deleting song {song_id}: {e}")
            raise

    @staticmethod
    def get_song_by_id(song_id: str) -> Optional[Dict[str, Any]]:
        """Get a song by ID."""
        try:
            song_obj_id = ObjectId(song_id)
            song = songs_collection.find_one({
                "_id": song_obj_id,
                "status": {"$ne": "deleted"}  # Exclude deleted songs
            })
            if song:
                song["_id"] = str(song["_id"])
            return song
        except Exception as e:
            logger.error(f"Error fetching song {song_id}: {e}")
            return None

    @staticmethod
    def get_songs_by_rass(rass: str) -> List[Dict[str, Any]]:
        """Get all active songs for a rass."""
        try:
            songs = list(songs_collection.find({
                "rass": rass.lower(),
                "status": {"$ne": "deleted"}
            }))
            return [{"_id": str(s["_id"]), **{k: v for k, v in s.items() if k != "_id"}} for s in songs]
        except Exception as e:
            logger.error(f"Error fetching songs for rass {rass}: {e}")
            raise

    @staticmethod
    def sync_songs_from_list(songs_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Bulk sync songs from a list (useful for Dropbox folder sync).

        Args:
            songs_data: List of song dictionaries with required fields

        Returns:
            Statistics of operation (created, updated, deleted)
        """
        stats = {
            "created": 0,
            "updated": 0,
            "deleted": 0,
            "errors": []
        }

        try:
            # Track which songs are in the new list
            new_song_names = {song.get("song_name") for song in songs_data}

            # Mark songs not in new list as deleted
            deleted_result = songs_collection.update_many(
                {
                    "song_name": {"$nin": list(new_song_names)},
                    "status": {"$ne": "deleted"}
                },
                {
                    "$set": {
                        "status": "deleted",
                        "deleted_at": datetime.now().isoformat()
                    }
                }
            )
            stats["deleted"] = deleted_result.modified_count

            # Insert or update songs
            for song_data in songs_data:
                try:
                    song_name = song_data.get("song_name")
                    existing = songs_collection.find_one({"song_name": song_name})

                    if existing:
                        # Update
                        song_data["updated_at"] = datetime.now().isoformat()
                        songs_collection.update_one(
                            {"song_name": song_name},
                            {"$set": song_data}
                        )
                        stats["updated"] += 1
                    else:
                        # Create
                        song_data["created_at"] = datetime.now().isoformat()
                        song_data["updated_at"] = datetime.now().isoformat()
                        song_data["status"] = "active"
                        if "ratings" not in song_data:
                            song_data["ratings"] = {"avg_rating": 0, "num_users": 0}
                        songs_collection.insert_one(song_data)
                        stats["created"] += 1

                except Exception as e:
                    logger.error(f"Error syncing song {song_data.get('song_name')}: {e}")
                    stats["errors"].append({
                        "song": song_data.get("song_name"),
                        "error": str(e)
                    })

            logger.info(f"Sync completed: Created {stats['created']}, Updated {stats['updated']}, Deleted {stats['deleted']}")
            return stats

        except Exception as e:
            logger.error(f"Error in bulk sync: {e}")
            raise

    @staticmethod
    def get_deleted_songs() -> List[Dict[str, Any]]:
        """Get all deleted songs."""
        try:
            songs = list(songs_collection.find({"status": "deleted"}))
            return [{"_id": str(s["_id"]), **{k: v for k, v in s.items() if k != "_id"}} for s in songs]
        except Exception as e:
            logger.error(f"Error fetching deleted songs: {e}")
            raise

    @staticmethod
    def restore_song(song_id: str) -> Optional[Dict[str, Any]]:
        """Restore a soft-deleted song."""
        try:
            song_obj_id = ObjectId(song_id)
            song = songs_collection.find_one_and_update(
                {"_id": song_obj_id},
                {
                    "$set": {
                        "status": "active",
                        "updated_at": datetime.now().isoformat()
                    },
                    "$unset": {"deleted_at": ""}
                },
                return_document=True
            )
            if song:
                song["_id"] = str(song["_id"])
                logger.info(f"Song restored: {song_id}")
            return song
        except Exception as e:
            logger.error(f"Error restoring song {song_id}: {e}")
            raise
