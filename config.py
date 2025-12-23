import os

# API Keys - Must be set via environment variables
GLADIA_API_KEY = os.getenv("GLADIA_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Recording settings
SAMPLE_RATE = 44100
BLOCK_DURATION_MINUTES = 10
RECORDINGS_DIR = "recordings"

# Gladia API settings
GLADIA_API_URL = "https://api.gladia.io/v2/transcription"
GLADIA_UPLOAD_URL = "https://api.gladia.io/v2/upload"

# Gemini settings
GEMINI_MODEL = "gemini-2.5-flash"
