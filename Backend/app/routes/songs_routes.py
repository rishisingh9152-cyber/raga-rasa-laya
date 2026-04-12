"""
Songs Routes: API endpoints for song streaming and recommendations.
Handles streaming URL generation and song retrieval.
"""

from fastapi import APIRouter, HTTPException, Path
from app.services.dropbox_service import get_dropbox_service
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/api/songs/stream/{song_id}")
def get_streaming_url(
    song_id: str = Path(
        ...,
        description="MongoDB song ID",
        min_length=24,
        max_length=24
    )
):
    """
    Get streaming URL for a specific song.
    
    Args:
        song_id: MongoDB ObjectId of the song (24-character hex string)
        
    Returns:
        JSON with song data and dropbox_url for streaming
        
    Example:
        GET /api/songs/stream/69bbd1896be7697a6bd9c507
        
        Response:
        {
            "song_id": "69bbd1896be7697a6bd9c507",
            "song_name": "Kamaj_amjadalikhan_shant.mp3",
            "rass": "shaant",
            "dropbox_url": "https://...",
            "avg_rating": 4.5,
            "num_users": 10
        }
    """
    try:
        dropbox_service = get_dropbox_service()
        song_data = dropbox_service.get_streaming_url(song_id)
        
        if not song_data:
            raise HTTPException(
                status_code=404,
                detail=f"Song not found: {song_id}"
            )
        
        return {
            "status": "success",
            "data": song_data
        }
        
    except ValueError as ve:
        logger.error(f"Invalid song_id: {song_id}, Error: {ve}")
        raise HTTPException(
            status_code=400,
            detail=str(ve)
        )
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        logger.error(f"Error getting streaming URL for {song_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/api/songs/rass/{rass}")
def get_songs_by_rass(
    rass: str = Path(
        ...,
        description="Rass name (shringar, shaant, veer, shok)",
        min_length=1
    )
):
    """
    Get all songs for a specific rass with streaming URLs.
    
    Args:
        rass: Rass name (shringar, shaant, veer, shok)
        
    Returns:
        JSON with list of songs and their streaming URLs
        
    Example:
        GET /api/songs/rass/shaant
        
        Response:
        {
            "status": "success",
            "rass": "shaant",
            "count": 32,
            "songs": [...]
        }
    """
    try:
        rass_lower = rass.lower().strip()
        
        # Validate rass
        valid_rasses = ["shringar", "shaant", "veer", "shok"]
        if rass_lower not in valid_rasses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid rass. Must be one of: {valid_rasses}"
            )
        
        dropbox_service = get_dropbox_service()
        songs = dropbox_service.get_all_songs_by_rass(rass_lower)
        
        if not songs:
            raise HTTPException(
                status_code=404,
                detail=f"No songs found for rass: {rass_lower}"
            )
        
        return {
            "status": "success",
            "rass": rass_lower,
            "count": len(songs),
            "songs": songs
        }
        
    except ValueError as ve:
        logger.error(f"Invalid rass: {rass}, Error: {ve}")
        raise HTTPException(
            status_code=400,
            detail=str(ve)
        )
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        logger.error(f"Error getting songs for rass {rass}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/api/songs/stats")
def get_songs_stats():
    """
    Get statistics about all songs in the database.
    
    Returns:
        JSON with total songs and breakdown by rass
        
    Example:
        GET /api/songs/stats
        
        Response:
        {
            "status": "success",
            "total_songs": 68,
            "by_rass": {
                "shringar": 7,
                "shaant": 32,
                "veer": 8,
                "shok": 21
            }
        }
    """
    try:
        dropbox_service = get_dropbox_service()
        stats = dropbox_service.get_mapping_stats()
        
        return {
            "status": "success",
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting songs stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
