import React from "react";

function Emotion({ setEmotion, setSongs, setCurrentSong }) {

  const detect = async () => {
    try {
      console.log("🎯 Calling emotion API...");

      // 1️⃣ Get emotion
      const res = await fetch("http://127.0.0.1:8000/emotion/live");
      const data = await res.json();

      console.log("🧠 Emotion response:", data);

      const emotion = data.emotion;

      // ❌ Handle bad cases
      if (!emotion || emotion === "no face detected" || emotion === "unknown") {
        alert("Face not detected properly. Try again.");
        return;
      }

      // ✅ Set emotion
      setEmotion(emotion);

      console.log("🎵 Fetching recommendations for:", emotion);

      // ✅ FIXED (template string)
      const songsRes = await fetch(
        `http://127.0.0.1:8000/recommendations?emotion=${emotion}`
      );

      const songsData = await songsRes.json();

      console.log("🎶 Songs response:", songsData);

      const recommendations = songsData?.recommendations || [];

      // 3️⃣ Set songs + play first
      if (recommendations.length > 0) {
        setSongs(recommendations);
        setCurrentSong(recommendations[0]);
      } else {
        alert("No recommendations received");
      }

    } catch (error) {
      console.error("❌ Error:", error);
      alert("Backend connection failed");
    }
  };

  return (
    <div>
      <button onClick={detect}>
        Detect Emotion 🎯
      </button>
    </div>
  );
}

export default Emotion;