import os

# Flask server settings
PORT = 5000

# Ngrok auth token
NGROK_TOKEN = os.getenv("NGROK_TOKEN", "")

# Model and inference settings
MODEL_PATH = os.getenv("MODEL_PATH", "./model/model-41.pt")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output_inference")
IMAGE_SIZE = 128
THRESHOLD = 100  # gray threshold for mask

# STAC / Planetary computer settings
BBOX_DELTA = 0.025

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
