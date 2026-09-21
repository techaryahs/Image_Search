from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


# Data
DATA_DIR = BASE_DIR / "data"

GOLD_DIR = DATA_DIR / "gold"

PROTOTYPE_DIR = DATA_DIR / "prototype"


# Embeddings
EMBEDDING_DIR = BASE_DIR / "embeddings"

GOLD_EMBEDDINGS_FILE = EMBEDDING_DIR / "gold_embeddings.npy"
GOLD_PATHS_FILE = EMBEDDING_DIR / "gold_paths.npy"
GOLD_INDEX_FILE = EMBEDDING_DIR / "gold.index"

PROTOTYPE_EMBEDDINGS_FILE = EMBEDDING_DIR / "prototype_embeddings.npy"
PROTOTYPE_PATHS_FILE = EMBEDDING_DIR / "prototype_paths.npy"
PROTOTYPE_INDEX_FILE = EMBEDDING_DIR / "prototype.index"


# DINOv2
MODEL_NAME = "facebook/dinov2-base"


TOP_K = 5

SIMILARITY_THRESHOLD = 0.80


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp"
}
