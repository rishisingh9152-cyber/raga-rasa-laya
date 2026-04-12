import React from "react";
import { getRecommendations } from "../services/api";

function Emotion({ setEmotion, setSongs, setCurrentSong }) {

  const detect = async () => {
    try {
      console.log("🎯 Getting recommendations for emotion: happy");

      // For now, hardcoded emotion (in future, integrate with camera/emotion detection)
      const emotion = "happy";

      // ✅ Set emotion
      setEmotion(emotion);

      console.log("🎵 Fetching recommendations from API...");

      // ✅ Use API service to get recommendations
      try {
        const recommendations = await getRecommendations(emotion, 5);

        console.log("🎶 Songs response:", recommendations);

        // ✅ Set songs + play first
        if (recommendations.length > 0) {
          setSongs(recommendations);
          setCurrentSong(recommendations[0]);
        } else {
          alert("No recommendations received. Check console for errors.");
        }
      } catch (apiError) {
        console.error("API Error:", apiError);
        alert(`Failed to fetch recommendations: ${apiError.message}`);
      }

    } catch (error) {
      console.error("❌ Error:", error);
      alert("Backend connection failed");
    }
  };

  return (
    <div>
      <button onClick={detect} style={{
        padding: "10px 20px",
        fontSize: "16px",
        backgroundColor: "#1DB954",
        color: "white",
        border: "none",
        borderRadius: "20px",
        cursor: "pointer"
      }}>
        Detect Emotion 🎯
      </button>
    </div>
  );
}

export default Emotion;