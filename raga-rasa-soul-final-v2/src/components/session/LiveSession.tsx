import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { useSession } from "@/context/SessionContext";
import { generateSensorData } from "@/services/mockData";
import { api, Song } from "@/services/api";
import {
  Camera,
  Thermometer,
  Music,
  RefreshCw,
  Square,
  Play,
  Pause,
  Scan,
  Loader2,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { toast } from "@/hooks/use-toast";

const LiveSession = () => {
  const {
    session,
    setStep,
    setCurrentEmotion,
    setCurrentRaga,
    setCurrentSongs,
    setCurrentSongId,
    setIsLoading,
  } = useSession();

  const [sensorData, setSensorData] = useState(generateSensorData());
  const [currentTemp, setCurrentTemp] = useState(36.5);
  const [emotionLog, setEmotionLog] = useState<string[]>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isDetecting, setIsDetecting] = useState(false);
  const [selectionStrategy, setSelectionStrategy] = useState<
    "exploration" | "fairness" | "exploitation" | null
  >(null);
  const [streamingUrl, setStreamingUrl] = useState<string>("");
  const [isLoadingStream, setIsLoadingStream] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Sensor data simulation
  useEffect(() => {
    const interval = setInterval(() => {
      const newTemp = 36 + Math.random() * 2;
      setCurrentTemp(newTemp);

      setSensorData((prev) => {
        const next = [
          ...prev.slice(1),
          {
            time: `${parseInt(prev[prev.length - 1].time) + 1}s`,
            temperature: newTemp,
            heartRate: 65 + Math.random() * 20,
          },
        ];
        return next;
      });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  // Fetch streaming URL when current song changes
  useEffect(() => {
    const fetchStreamingUrl = async () => {
      if (!session.currentSongId) {
        setStreamingUrl("");
        return;
      }

      setIsLoadingStream(true);
      try {
        const response = await api.getStreamingUrl(session.currentSongId);
        if (response && response.data && response.data.dropbox_url) {
          setStreamingUrl(response.data.dropbox_url);
        } else {
          // Fallback to legacy audio URL if streaming URL not available
          const currentSong = session.currentSongs.find(
            (s) =>
              s._id === session.currentSongId ||
              s.song_id === session.currentSongId
          );
          if (currentSong) {
            setStreamingUrl(api.getAudioUrl(currentSong.file_path));
          }
        }
      } catch (error) {
        console.error("Error fetching streaming URL:", error);
        // Fallback to legacy audio URL
        const currentSong = session.currentSongs.find(
          (s) =>
            s._id === session.currentSongId ||
            s.song_id === session.currentSongId
        );
        if (currentSong) {
          setStreamingUrl(api.getAudioUrl(currentSong.file_path));
        }
      } finally {
        setIsLoadingStream(false);
      }
    };

    fetchStreamingUrl();
  }, [session.currentSongId]);

  // Hybrid emotion detection and recommendation with psychometric fusion
  const detectAndRecommend = async () => {
    setIsDetecting(true);

    try {
      // Step 1: Detect emotion from camera
      const emotionData = await api.detectEmotion();

      if (emotionData.error) {
        throw new Error(emotionData.error);
      }

      const emotion = emotionData.emotion;

      await setCurrentEmotion(emotion);

      setEmotionLog((prev) => [...prev.slice(-4), emotion]);

      // Step 2: Get psychometric data from session
      const preTest = session.preTestResults || {
        reactionTime: 500,
        memoryScore: 5,
        moodLevel: 5,
      };

      const recommendations = await api.getHybridRecommendations(
        emotion,
        preTest,
        5
      );

      // Step 3: Get HYBRID recommendations

      if (
        recommendations.recommendations &&
        recommendations.recommendations.length > 0
      ) {
        const songs = recommendations.recommendations;

        setCurrentSongs(songs);

        const firstSong = songs[0];

        setCurrentRaga(firstSong.song_name);
        setCurrentSongId(firstSong.song_id || firstSong._id);

        // Show selection strategy used
        if (recommendations.selection_strategy) {
          setSelectionStrategy(
            recommendations.selection_strategy as any
          );
        }

        const strategyLabel = {
          exploration: "🎲 Exploring new songs",
          fairness: "⚖️ Fair recommendation",
          exploitation: "⭐ Best match",
        }[
          recommendations.selection_strategy || "exploitation"
        ];

        toast({
          title: `Detected: ${emotion}`,
          description: `${strategyLabel} - Recommended: ${firstSong.song_name}`,
        });
      }
    } catch (error: any) {
      console.error("Detection error:", error);

      // Fallback to legacy recommendations if hybrid fails
      try {
        console.log("Falling back to legacy recommendations...");

        const emotion = session.currentEmotion;

        const recommendations = await api.getRecommendations(emotion);

        if (recommendations.recommendations?.length > 0) {
          const songs = recommendations.recommendations;

          setCurrentSongs(songs);

          const firstSong = songs[0];

          setCurrentRaga(firstSong.song_name);
          setCurrentSongId(firstSong.song_id || firstSong._id);
        }
      } catch (fallbackError) {
        toast({
          title: "Detection Note",
          description:
            error.message ||
            "Could not connect to camera/recommendations.",
          variant: "default",
        });
      }
    } finally {
      setIsDetecting(false);
    }
  };

  // Initial detection + periodic re-detection
  useEffect(() => {
    detectAndRecommend();

    const interval = setInterval(detectAndRecommend, 15000);

    return () => clearInterval(interval);
  }, []);

  const currentSong = session.currentSongs.find(
    (s) =>
      s._id === session.currentSongId ||
      s.song_id === session.currentSongId
  ) as Song | undefined;

  const togglePlay = () => {
    if (!audioRef.current || !currentSong) return;

    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }

    setIsPlaying(!isPlaying);
  };

  const changeRaga = () => {
    if (session.currentSongs.length > 1) {
      const currentIndex = session.currentSongs.findIndex(
        (s) =>
          s._id === session.currentSongId ||
          s.song_id === session.currentSongId
      );

      const nextIndex =
        (currentIndex + 1) % session.currentSongs.length;

      const nextSong = session.currentSongs[nextIndex];

      setCurrentRaga(nextSong.song_name);
      setCurrentSongId(nextSong.song_id || nextSong._id);
      setIsPlaying(false);
    } else {
      detectAndRecommend();
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-4 sm:space-y-6 pb-6">
      {currentSong && (
        <audio
          ref={audioRef}
          src={streamingUrl || api.getAudioUrl(currentSong.file_path)}
          onEnded={() => setIsPlaying(false)}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
        />
      )}

      {/* Top: Current emotion + Suggested Raga */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
        {/* ... ENTIRE UI REMAINS EXACTLY SAME ... */}
      </div>
    </div>
  );
};

export default LiveSession;