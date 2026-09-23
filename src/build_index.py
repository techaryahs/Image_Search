from pathlib import Path
import numpy as np
import faiss
from tqdm import tqdm

from src.config import (
    EMBEDDING_DIR,
    GOLD_DIR,
    GOLD_EMBEDDINGS_FILE,
    GOLD_PATHS_FILE,
    GOLD_INDEX_FILE,
    PROTOTYPE_DIR,
    PROTOTYPE_EMBEDDINGS_FILE,
    PROTOTYPE_PATHS_FILE,
    PROTOTYPE_INDEX_FILE,
)

from src.image_utils import (
    get_image_paths,
    load_image,
)

from src.model import ImageEncoder


def build_faiss_index(
    image_directory: Path,
    embedding_output_file: Path,
    paths_output_file: Path,
    index_output_file: Path,
    encoder: ImageEncoder = None,
    label: str = "INDEX",
):
    """
    Generic function to build a FAISS index for images in a given directory.
    """
    print("=" * 60)
    print(f"BUILDING {label.upper()}")
    print("=" * 60)

    # Ensure embeddings directory exists
    EMBEDDING_DIR.mkdir(parents=True, exist_ok=True)

    image_paths = get_image_paths(image_directory)

    if not image_paths:
        print(f"\nNo images found in: {image_directory}")
        return False

    print(f"\nFound {len(image_paths)} images in {image_directory.name}.")

    if encoder is None:
        encoder = ImageEncoder()

    embeddings = []
    valid_paths = []

    print("\nCreating embeddings...")

    for image_path in tqdm(image_paths, desc=f"Processing {label}"):
        try:
            image = load_image(image_path)
            embedding = encoder.encode_image(image)
            embeddings.append(embedding)
            valid_paths.append(str(image_path))
        except Exception as e:
            print(f"\nSkipping invalid image: {image_path}")
            print(f"Error: {e}")

    if not embeddings:
        print(f"\nNo valid embeddings created for {label}.")
        return False

    # Convert to NumPy array
    embeddings_np = np.array(embeddings, dtype=np.float32)
    print(f"\nEmbedding shape: {embeddings_np.shape}")

    # L2 Normalization
    faiss.normalize_L2(embeddings_np)

    # Create FAISS Index (Inner Product on L2-normalized vectors = Cosine Similarity)
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings_np)

    # Save artifacts
    np.save(embedding_output_file, embeddings_np)
    np.save(paths_output_file, np.array(valid_paths))
    faiss.write_index(index, str(index_output_file))

    print(f"\n{label} FAISS index created successfully.")
    return True


def build_gold_index(encoder: ImageEncoder = None):
    """
    Build FAISS index for Gold product images.
    """
    return build_faiss_index(
        image_directory=GOLD_DIR,
        embedding_output_file=GOLD_EMBEDDINGS_FILE,
        paths_output_file=GOLD_PATHS_FILE,
        index_output_file=GOLD_INDEX_FILE,
        encoder=encoder,
        label="GOLD INDEX",
    )


def build_prototype_index(encoder: ImageEncoder = None):
    """
    Build FAISS index for Prototype images.
    """
    return build_faiss_index(
        image_directory=PROTOTYPE_DIR,
        embedding_output_file=PROTOTYPE_EMBEDDINGS_FILE,
        paths_output_file=PROTOTYPE_PATHS_FILE,
        index_output_file=PROTOTYPE_INDEX_FILE,
        encoder=encoder,
        label="PROTOTYPE INDEX",
    )


def build_all_indexes():
    """
    Build both Gold and Prototype FAISS indexes.
    """
    encoder = ImageEncoder()
    build_gold_index(encoder=encoder)
    print()
    build_prototype_index(encoder=encoder)
    print("\n" + "=" * 60)
    print("INDEX BUILD COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    build_all_indexes()