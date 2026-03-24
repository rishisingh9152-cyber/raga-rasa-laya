import { useState } from "react";
import Emotion from "./components/Emotion";
import Player from "./components/Player";
import Rating from "./components/Rating";
import Upload from "./components/Upload";

function App() {
  const [emotion, setEmotion] = useState("");
  const [songs, setSongs] = useState([]);
  const [songIndex, setSongIndex] = useState(0);
  const [currentSong, setCurrentSong] = useState(null);
  const [showRating, setShowRating] = useState(false);

  // 🔥 Next Song
  const nextSong = () => {
    if (songs.length === 0) return;

    setSongIndex((prevIndex) => {
      const nextIndex = (prevIndex + 1) % songs.length;
      setCurrentSong(songs[nextIndex]);
      return nextIndex;
    });

    setShowRating(false);
  };

  // 🔥 Previous Song
  const prevSong = () => {
    if (songs.length === 0) return;

    const prevIndex =
      (songIndex - 1 + songs.length) % songs.length;

    setSongIndex(prevIndex);
    setCurrentSong(songs[prevIndex]);
    setShowRating(false);
  };

  return (
    <div
      style={{
        textAlign: "center",
        background: "#121212",
        color: "white",
        minHeight: "100vh",
        paddingTop: "40px",
      }}
    >
      <h1>🎵 AI Music Player</h1>

      {/* ✅ Upload Section */}
      <Upload />

      {/* Optional separator */}
      <hr style={{ margin: "20px 0", opacity: 0.3 }} />

      {/* Emotion Selection */}
      <Emotion
        setEmotion={setEmotion}
        setSongs={(songsData) => {
          setSongs(songsData);
          setSongIndex(0);
          setCurrentSong(songsData[0]); // autoplay first song
        }}
      />

      {emotion && <h2>Emotion: {emotion}</h2>}

      {/* Player */}
      {currentSong && (
        <Player
          song={currentSong}
          setShowRating={setShowRating}
          showRating={showRating}
          onLowRating={nextSong}
          onNext={nextSong}
          onPrev={prevSong}
        />
      )}

      {/* Rating */}
      {showRating && currentSong && (
        <Rating
          song={currentSong}
          onLowRating={nextSong}
        />
      )}
    </div>
  );
}

export default App;