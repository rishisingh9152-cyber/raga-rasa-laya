import os
import numpy as np
import librosa
from tensorflow.keras.models import load_model

# ----------------------------
# Load model
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "raas_cnn_model.h5")

model = load_model(MODEL_PATH)

RASS_LABELS = ["shaant", "shok", "shringar", "veer"]


# ----------------------------
# Feature Extraction
# ----------------------------
def extract_mel_spectrogram(file_path, max_len=128):
    y, sr = librosa.load(file_path, sr=22050)

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_mels=128,
        fmax=8000
    )

    mel_db = librosa.power_to_db(mel)

    mel_db = (mel_db - np.mean(mel_db)) / (np.std(mel_db) + 1e-6)

    if mel_db.shape[1] < max_len:
        pad_width = max_len - mel_db.shape[1]
        mel_db = np.pad(mel_db, ((0, 0), (0, pad_width)))
    else:
        mel_db = mel_db[:, :max_len]

    return mel_db


# ----------------------------
# Prediction
# ----------------------------
def predict(file_path):
    mel = extract_mel_spectrogram(file_path)

    mel = mel[np.newaxis, ..., np.newaxis]

    prediction = model.predict(mel, verbose=0)

    class_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    rass = RASS_LABELS[class_index]

    return rass, prediction.tolist(), confidence