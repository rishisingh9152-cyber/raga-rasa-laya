import React, { useState } from "react";

function Rating({ song, onLowRating }) {

  const [rating, setRating] = useState(0);

  const submitRating = async () => {

    await fetch("http://127.0.0.1:8000/rate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        song_id: song._id,
        rating: rating
      })
    });

    if (rating < 3) {
      onLowRating(); // 🔥 change song
    }
  };

  return (
    <div>
      <h3>Rate this song</h3>

      <input
        type="number"
        min="1"
        max="5"
        onChange={(e) => setRating(Number(e.target.value))}
      />

      <button onClick={submitRating}>Submit</button>
    </div>
  );
}

export default Rating;