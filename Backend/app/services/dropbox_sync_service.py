"""
DropboxSyncService: Monitors and syncs songs from Dropbox folder.
Provides methods to scan Dropbox, detect changes, and update database.
"""

from typing import List, Dict, Any, Optional
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DropboxSyncService:
    """Service for syncing songs from Dropbox folder."""

    # Dropbox folder structure
    RASS_FOLDERS = {
        "shringar": "Shringar",
        "shaant": "Shaant",
        "veer": "Veer",
        "shok": "Shok"
    }

    DROPBOX_FOLDER_ID = "2je1qltlw5zuhosbd96zf"
    DROPBOX_BASE_URL = "https://www.dropbox.com/scl/fo/2je1qltlw5zuhosbd96zf"

    # Supported audio formats
    SUPPORTED_FORMATS = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"}

    @staticmethod
    def get_dropbox_songs() -> List[Dict[str, Any]]:
        """
        Get list of songs from Dropbox folder structure.

        Returns:
            List of song dictionaries with metadata
        """
        songs = []

        try:
            # In production, this would use Dropbox API
            # For now, we'll return a structure that can be populated
            logger.info("Scanning Dropbox folder for songs...")

            # Example structure - in production would call Dropbox API
            # to get actual file listing from the shared folder
            
            return songs

        except Exception as e:
            logger.error(f"Error scanning Dropbox folder: {e}")
            raise

    @staticmethod
    def build_song_from_dropbox_file(
        filename: str,
        dropbox_path: str,
        rass: str
    ) -> Optional[Dict[str, Any]]:
        """
        Build song document from Dropbox file info.

        Args:
            filename: Name of the file
            dropbox_path: Path in Dropbox (e.g., "/Shaant/song.mp3")
            rass: Rasa type

        Returns:
            Song document or None if invalid
        """
        try:
            # Check if it's an audio file
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in DropboxSyncService.SUPPORTED_FORMATS:
                return None

            # Get duration and other metadata (would use audio processing library)
            song_doc = {
                "song_name": filename,
                "rass": rass.lower(),
                "file_path": dropbox_path,
                "dropbox_path": dropbox_path,
                "dropbox_url": DropboxSyncService.build_dropbox_download_url(dropbox_path),
                "features": [],
                "confidence": 0.5,
                "ratings": {
                    "avg_rating": 0,
                    "num_users": 0
                },
                "metadata": {
                    "source": "dropbox",
                    "format": file_ext.strip(".").upper(),
                    "last_scanned": datetime.now().isoformat()
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "active"
            }

            return song_doc

        except Exception as e:
            logger.error(f"Error building song from Dropbox file {filename}: {e}")
            return None

    @staticmethod
    def build_dropbox_download_url(dropbox_path: str) -> str:
        """
        Build Dropbox download URL for a file.

        Args:
            dropbox_path: Path in Dropbox folder

        Returns:
            Download URL with ?dl=1 parameter
        """
        try:
            # In production, this would use Dropbox API to get sharing links
            # For now, use direct URL pattern
            path = dropbox_path.replace("\\", "/").strip("/")
            folder_id = DropboxSyncService.DROPBOX_FOLDER_ID
            
            # This is a template URL - actual implementation would use Dropbox API
            # to get proper file IDs and sharing links
            return f"https://www.dropbox.com/scl/fo/{folder_id}/{path}?dl=1"

        except Exception as e:
            logger.error(f"Error building Dropbox URL for {dropbox_path}: {e}")
            return ""

    @staticmethod
    def scan_local_dropbox_folder(dropbox_folder_path: str) -> List[Dict[str, Any]]:
        """
        Scan local Dropbox folder for songs (alternative to API).
        
        Args:
            dropbox_folder_path: Local path to Dropbox folder
                                 (e.g., "C:/Users/user/Dropbox/RagaRasa")

        Returns:
            List of song documents
        """
        songs = []

        try:
            if not os.path.isdir(dropbox_folder_path):
                logger.error(f"Dropbox folder not found: {dropbox_folder_path}")
                return songs

            logger.info(f"Scanning local Dropbox folder: {dropbox_folder_path}")

            # Scan each rass subfolder
            for rass, folder_name in DropboxSyncService.RASS_FOLDERS.items():
                rass_path = os.path.join(dropbox_folder_path, folder_name)

                if not os.path.isdir(rass_path):
                    logger.warning(f"Rass folder not found: {rass_path}")
                    continue

                # Scan for audio files in this rass folder
                for filename in os.listdir(rass_path):
                    file_path = os.path.join(rass_path, filename)

                    # Skip directories
                    if os.path.isdir(file_path):
                        continue

                    # Check if it's an audio file
                    file_ext = os.path.splitext(filename)[1].lower()
                    if file_ext not in DropboxSyncService.SUPPORTED_FORMATS:
                        continue

                    # Build Dropbox path
                    dropbox_relative_path = f"/{folder_name}/{filename}"

                    # Create song document
                    song = DropboxSyncService.build_song_from_dropbox_file(
                        filename,
                        dropbox_relative_path,
                        rass
                    )

                    if song:
                        songs.append(song)
                        logger.info(f"Found song: {rass}/{filename}")

            logger.info(f"Scan complete: Found {len(songs)} songs")
            return songs

        except Exception as e:
            logger.error(f"Error scanning Dropbox folder: {e}")
            raise

    @staticmethod
    def sync_with_dropbox(
        dropbox_folder_path: str,
        sync_service_callback=None
    ) -> Dict[str, Any]:
        """
        Sync database with Dropbox folder contents.

        Args:
            dropbox_folder_path: Local path to Dropbox folder
            sync_service_callback: Optional callback function from SongManagementService

        Returns:
            Sync statistics
        """
        try:
            # Scan Dropbox folder for songs
            songs = DropboxSyncService.scan_local_dropbox_folder(dropbox_folder_path)

            if not songs:
                logger.warning("No songs found in Dropbox folder")
                return {
                    "created": 0,
                    "updated": 0,
                    "deleted": 0,
                    "errors": ["No songs found in Dropbox folder"]
                }

            # If callback provided, use it to sync with database
            if sync_service_callback:
                stats = sync_service_callback(songs)
                return stats

            return {
                "created": 0,
                "updated": 0,
                "deleted": 0,
                "message": "Songs scanned but not synced (no callback provided)"
            }

        except Exception as e:
            logger.error(f"Error syncing with Dropbox: {e}")
            raise

    @staticmethod
    def get_sync_status() -> Dict[str, Any]:
        """
        Get status of Dropbox sync service.

        Returns:
            Service status information
        """
        return {
            "service": "DropboxSyncService",
            "status": "active",
            "last_sync": None,  # Would track in database
            "supported_formats": list(DropboxSyncService.SUPPORTED_FORMATS),
            "rass_folders": DropboxSyncService.RASS_FOLDERS,
            "dropbox_folder_id": DropboxSyncService.DROPBOX_FOLDER_ID
        }
