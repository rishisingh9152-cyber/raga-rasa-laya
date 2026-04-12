"""
DropboxService: Manages Dropbox streaming URLs for songs.
Maps song_ids to Dropbox streaming URLs on-demand.
"""

from typing import Optional, Dict, Any
from app.database import songs_collection
import logging

logger = logging.getLogger(__name__)


class DropboxService:
    """Service for managing Dropbox streaming URLs."""
    
    # Base Dropbox folder - shared folder link
    DROPBOX_FOLDER_ID = "2je1qltlw5zuhosbd96zf"
    
    @staticmethod
    def build_dropbox_url(dropbox_path: str) -> str:
        """
        Build Dropbox streaming URL from dropbox_path.
        
        Example:
            dropbox_path = "/Shringar/Song1.mp3"
            returns: "https://dl.dropboxusercontent.com/scl/fi/.../Song1.mp3?dl=1"
        
        Args:
            dropbox_path: File path in Dropbox (e.g., "/Shringar/Song1.mp3")
            
        Returns:
            Full Dropbox streaming URL with ?dl=1 for streaming
        """
        # For now, we'll store raw paths in MongoDB and build URLs on request
        # In a real scenario, you'd have the full Dropbox file IDs
        if not dropbox_path:
            return None
        
        # Replace backslashes with forward slashes
        dropbox_path = dropbox_path.replace("\\", "/")
        
        # Remove leading slash if present
        if dropbox_path.startswith("/"):
            dropbox_path = dropbox_path[1:]
        
        # Construct Dropbox sharing link (this is a template)
        # Real implementation would use Dropbox API to get sharing links
        return f"https://www.dropbox.com/scl/fo/{DropboxService.DROPBOX_FOLDER_ID}/download?rlkey=...&dl=1"
    
    @staticmethod
    def get_streaming_url(song_id: str) -> Optional[Dict[str, Any]]:
        """
        Get streaming URL for a specific song by ID.
        
        Args:
            song_id: MongoDB song ID (string)
            
        Returns:
            Dict with song data and dropbox_url, or None if not found
            
        Raises:
            ValueError: If song_id is invalid
        """
        from bson import ObjectId
        
        if not song_id:
            raise ValueError("song_id cannot be empty")
        
        try:
            # Convert string ID to ObjectId
            song_obj_id = ObjectId(song_id)
        except Exception as e:
            logger.error(f"Invalid song_id format: {song_id}, Error: {e}")
            raise ValueError(f"Invalid song_id format: {song_id}")
        
        try:
            song = songs_collection.find_one({"_id": song_obj_id})
            
            if not song:
                logger.warning(f"Song not found: {song_id}")
                return None
            
            # Build response with streaming URL
            response = {
                "song_id": str(song["_id"]),
                "song_name": song.get("song_name", "Unknown"),
                "rass": song.get("rass", "unknown"),
                "file_path": song.get("file_path", ""),
                "dropbox_url": DropboxService.build_dropbox_url(
                    song.get("file_path", "")
                ),
                "avg_rating": float(song.get("ratings", {}).get("avg_rating", 0)),
                "num_users": int(song.get("ratings", {}).get("num_users", 0))
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error fetching song {song_id}: {e}")
            raise
    
    @staticmethod
    def get_all_songs_by_rass(rass: str) -> list:
        """
        Get all songs for a specific rass with streaming URLs.
        
        Args:
            rass: Rass name (e.g., "shringar", "shaant", "veer", "shok")
            
        Returns:
            List of songs with streaming URLs
        """
        if not rass:
            raise ValueError("rass cannot be empty")
        
        try:
            songs = list(songs_collection.find({"rass": rass.lower()}))
            
            response = []
            for song in songs:
                response.append({
                    "song_id": str(song["_id"]),
                    "song_name": song.get("song_name", "Unknown"),
                    "rass": song.get("rass", "unknown"),
                    "file_path": song.get("file_path", ""),
                    "dropbox_url": DropboxService.build_dropbox_url(
                        song.get("file_path", "")
                    ),
                    "avg_rating": float(song.get("ratings", {}).get("avg_rating", 0)),
                    "num_users": int(song.get("ratings", {}).get("num_users", 0))
                })
            
            return response
            
        except Exception as e:
            logger.error(f"Error fetching songs for rass {rass}: {e}")
            raise
    
    @staticmethod
    def get_mapping_stats() -> Dict[str, Any]:
        """
        Get statistics about all songs in the database.
        
        Returns:
            Dictionary with counts by rass
        """
        try:
            stats = {}
            
            # Count songs by rass
            pipeline = [
                {"$group": {"_id": "$rass", "count": {"$sum": 1}}}
            ]
            
            results = list(songs_collection.aggregate(pipeline))
            
            for result in results:
                rass = result.get("_id", "unknown")
                count = result.get("count", 0)
                stats[rass] = count
            
            return {
                "total_songs": sum(stats.values()),
                "by_rass": stats
            }
            
        except Exception as e:
            logger.error(f"Error getting mapping stats: {e}")
            raise


# Global instance initialization
_dropbox_service = None


def init_dropbox_service():
    """Initialize the Dropbox service."""
    global _dropbox_service
    _dropbox_service = DropboxService()
    logger.info("DropboxService initialized")


def get_dropbox_service() -> DropboxService:
    """Get the global DropboxService instance."""
    if _dropbox_service is None:
        init_dropbox_service()
    return _dropbox_service
