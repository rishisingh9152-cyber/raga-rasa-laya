const BASE_URL = "http://127.0.0.1:8000";

// ==============================
// INTERFACES
// ==============================
export interface Song {
  song_id?: string;
  _id?: string;
  song_name: string;
  rass: string;
  file_path: string;
  avg_rating?: number;
  num_users?: number;
  confidence?: number;
  final_rank_score?: number;
  fairness_boost?: number;
  confidence_score?: number;
}

export interface EmotionResponse {
  emotion: string;
  image_path: string;
}

export interface RecommendationResponse {
  status: string;
  user_id: string;
  emotion: string;
  count: number;
  recommendations: Song[];
  rass?: string;
  fusion?: any;
  selection_strategy?: string;
}

export interface PsychometricResult {
  reactionTime: number;
  memoryScore: number;
  moodLevel: number;
}

export interface PsychometricResponse {
  status: string;
  test_id: string;
  message: string;
}

export interface SessionResponse {
  status: string;
  session_id: string;
}

export interface StreamingUrlResponse {
  status: string;
  data: {
    song_id: string;
    song_name: string;
    rass: string;
    file_path: string;
    dropbox_url: string;
    avg_rating: number;
    num_users: number;
  };
}

// ==============================
// API SERVICE
// ==============================
export const api = {
  // ============================
  // EMOTION
  // ============================
  async detectEmotion(): Promise<EmotionResponse> {
    const response = await fetch(`${BASE_URL}/emotion/live`);
    if (!response.ok) throw new Error("Failed to detect emotion");
    return response.json();
  },

  // ============================
  // PSYCHOMETRIC
  // ============================
  async savePsychometricPreTest(
    data: PsychometricResult,
    sessionId?: string
  ): Promise<PsychometricResponse> {
    const response = await fetch(`${BASE_URL}/psychometric/pre-test`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        reaction_time_ms: data.reactionTime,
        memory_score: data.memoryScore,
        mood_level: data.moodLevel,
        user_id: "default_user",
        session_id: sessionId,
      }),
    });

    if (!response.ok) throw new Error("Failed to save pre-test");
    return response.json();
  },

  async savePsychometricPostTest(
    data: PsychometricResult,
    sessionId?: string
  ): Promise<PsychometricResponse> {
    const response = await fetch(`${BASE_URL}/psychometric/post-test`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        reaction_time_ms: data.reactionTime,
        memory_score: data.memoryScore,
        mood_level: data.moodLevel,
        user_id: "default_user",
        session_id: sessionId,
      }),
    });

    if (!response.ok) throw new Error("Failed to save post-test");
    return response.json();
  },

  // ============================
  // SESSIONS
  // ============================
  async createSession(preTestId?: string): Promise<SessionResponse> {
    const response = await fetch(`${BASE_URL}/sessions/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: "default_user",
        pre_test_id: preTestId,
      }),
    });

    if (!response.ok) throw new Error("Failed to create session");
    return response.json();
  },

  // ============================
  // ✅ HYBRID RECOMMENDATION (FINAL FIX)
  // ============================
  async getHybridRecommendations(
    emotion: string,
    preTest: any,
    limit: number
  ): Promise<Song[]> {
    const response = await fetch(
      `${BASE_URL}/songs/recommend/hybrid`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          emotion: emotion.toLowerCase(),
          reaction_time_ms: preTest?.reactionTime || 500,
          memory_score: preTest?.memoryScore || 5,
          mood_level: preTest?.moodLevel || 5,
          emotion_confidence: 0.85,
          limit: limit,
          user_id: "default_user",
        }),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to fetch hybrid recommendations");
    }

    const data = await response.json();

    console.log("Hybrid API response:", data);

    if (!data || !Array.isArray(data.recommendations)) {
      throw new Error("Invalid hybrid response");
    }

    return data.recommendations;
  },

  // ============================
  // LEGACY (OPTIONAL)
  // ============================
  async getRecommendations(
    emotion: string
  ): Promise<RecommendationResponse> {
    const response = await fetch(
      `${BASE_URL}/recommendations?emotion=${emotion}`
    );

    if (!response.ok) throw new Error("Failed to fetch recommendations");
    return response.json();
  },

  // ============================
  // AUDIO
  // ============================
  getAudioUrl(filePath: string): string {
    const filename = filePath.split(/[\\/]/).pop();
    return `${BASE_URL}/songs/${filename}`;
  },

  // ============================
  // STREAMING (DROPBOX)
  // ============================
  async getStreamingUrl(songId: string): Promise<StreamingUrlResponse> {
    const response = await fetch(`${BASE_URL}/api/songs/stream/${songId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch streaming URL for song ${songId}`);
    }
    return response.json();
  },

  async getSongsByRass(rass: string): Promise<any> {
    const response = await fetch(`${BASE_URL}/api/songs/rass/${rass}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch songs for rass: ${rass}`);
    }
    return response.json();
  },

  async getSongsStats(): Promise<any> {
    const response = await fetch(`${BASE_URL}/api/songs/stats`);
    if (!response.ok) {
      throw new Error("Failed to fetch songs stats");
    }
    return response.json();
  },
};