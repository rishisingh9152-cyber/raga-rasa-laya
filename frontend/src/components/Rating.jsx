import React, { useState } from "react";
import { rateSong } from "../services/api";

function Rating({ song, onLowRating }) {

  const [rating, setRating] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const submitRating = async () => {
    if (rating < 1 || rating > 5) {
      alert("Please select a rating between 1 and 5");
      return;
    }

    setIsSubmitting(true);
    
    try {
      // Use song_name or song._id for identification
      const songId = song.song_name || song._id || "unknown";
      const userId = "user_" + Date.now(); // Generate a unique user ID
      
      await rateSong(songId, userId, rating);
      
      console.log("✅ Rating submitted successfully");
      
      // If rating is low, skip to next song
      if (rating < 3) {
        alert("Rating submitted. Moving to next song...");
        onLowRating();
      } else {
        alert("Thank you for your rating!");
      }
      
      setRating(0);
    } catch (error) {
      console.error("❌ Error submitting rating:", error);
      alert("Failed to submit rating: " + error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{
      background: "#1DB954",
      color: "white",
      padding: "20px",
      borderRadius: "10px",
      margin: "20px 0",
      textAlign: "center"
    }}>
      <h3>Rate this song</h3>

      <div style={{ marginBottom: "10px" }}>
        <input
          type="number"
          min="1"
          max="5"
          value={rating}
          onChange={(e) => setRating(Number(e.target.value))}
          style={{
            padding: "10px",
            fontSize: "16px",
            borderRadius: "5px",
            border: "none",
            width: "60px",
            textAlign: "center"
          }}
          disabled={isSubmitting}
        />
        <span style={{ marginLeft: "10px", fontSize: "14px" }}>/ 5</span>
      </div>

      <button 
        onClick={submitRating}
        disabled={isSubmitting || rating === 0}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: isSubmitting ? "#888" : "#121212",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: isSubmitting ? "not-allowed" : "pointer"
        }}
      >
        {isSubmitting ? "Submitting..." : "Submit Rating"}
      </button>
    </div>
  );
}

export default Rating;