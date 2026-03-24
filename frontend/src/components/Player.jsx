import React, { useEffect } from "react";
import Rating from "./Rating";

function Player({ song, setShowRating, showRating, onLowRating, onNext, onPrev }) {

  useEffect(() => {
    if (!song) return;

    const timer = setTimeout(() => {
      setShowRating(true);
    }, 5 * 60 * 1000);

    return () => clearTimeout(timer);
  }, [song]);

  if (!song) return null;

  const url = `http://127.0.0.1:8000/songs/${song.rass}/${song.song_name}`;

  return (
    <div style={{
      background: "#121212",
      color: "white",
      padding: "30px",
      borderRadius: "20px",
      width: "350px",
      margin: "40px auto",
      textAlign: "center",
      boxShadow: "0 0 20px rgba(0,0,0,0.5)"
    }}>
      <h2>🎧Raga Laya Rasa</h2>

      <p style={{ fontSize: "18px" }}>
        {song.song_name}
      </p>

      <audio controls autoPlay style={{ width: "100%" }}>
        <source src={url} type="audio/mp3" />
      </audio>

      <br /><br />

      {/* Controls */}
      <div>
        <button onClick={onPrev}>⏮️</button>
        <button onClick={onNext}>⏭️</button>
      </div>

      <br />

      <button onClick={() => setShowRating(true)}>
        Rate Now ⭐
      </button>

      {showRating && (
        <Rating song={song} onLowRating={onLowRating} />
      )}
    </div>
  );
}

export default Player;