from typing import Dict, List, Any
import faiss
import numpy as np
from PIL import Image

from src.config import (
    GOLD_INDEX_FILE,
    GOLD_PATHS_FILE,
    PROTOTYPE_INDEX_FILE,
    PROTOTYPE_PATHS_FILE,
    TOP_K,
)

from src.model import ImageEncoder, get_encoder


class BidirectionalJewelrySearch:

    def __init__(self, encoder: ImageEncoder = None):
        print("Loading Bidirectional Jewelry Search Engine...")
        self.encoder = encoder if encoder is not None else get_encoder()
        self.load_indexes()

    def load_indexes(self):
        """
        Load or reload FAISS indexes and path arrays.
        """
        # Load Gold index
        if GOLD_INDEX_FILE.exists() and GOLD_PATHS_FILE.exists():
            self.gold_index = faiss.read_index(str(GOLD_INDEX_FILE))
            self.gold_paths = np.load(GOLD_PATHS_FILE, allow_pickle=True)
            print(f"Loaded Gold index with {self.gold_index.ntotal} products.")
        else:
            self.gold_index = None
            self.gold_paths = np.array([])
            print("Gold index file not found.")

        # Load Prototype index
        if PROTOTYPE_INDEX_FILE.exists() and PROTOTYPE_PATHS_FILE.exists():
            self.prototype_index = faiss.read_index(str(PROTOTYPE_INDEX_FILE))
            self.prototype_paths = np.load(PROTOTYPE_PATHS_FILE, allow_pickle=True)
            print(f"Loaded Prototype index with {self.prototype_index.ntotal} prototypes.")
        else:
            self.prototype_index = None
            self.prototype_paths = np.array([])
            print("Prototype index file not found.")

    def _search(
        self,
        query_image: Image.Image,
        index: faiss.Index,
        image_paths: np.ndarray,
        top_k: int = TOP_K,
    ) -> List[Dict[str, Any]]:
        """
        Generic search internal method against a FAISS index.
        """
        if index is None or len(image_paths) == 0:
            return []

        # Convert query image to 1536-D embedding using DINOv2Encoder
        query_embedding = self.encoder.encode_image(query_image)

        # Convert to NumPy float32
        query_embedding = np.array([query_embedding], dtype=np.float32)

        # Normalize L2
        faiss.normalize_L2(query_embedding)

        # Search FAISS
        actual_k = min(top_k, index.ntotal)
        if actual_k <= 0:
            return []

        scores, indices = index.search(query_embedding, actual_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            results.append(
                {
                    "image_path": str(image_paths[idx]),
                    "similarity": float(score),
                }
            )

        return results

    def search_gold(
        self, query_image: Image.Image, top_k: int = TOP_K
    ) -> List[Dict[str, Any]]:
        """
        Search Gold index using a Prototype query image.
        """
        return self._search(
            query_image=query_image,
            index=self.gold_index,
            image_paths=self.gold_paths,
            top_k=top_k,
        )

    def search_prototype(
        self, query_image: Image.Image, top_k: int = TOP_K
    ) -> List[Dict[str, Any]]:
        """
        Search Prototype index using a Gold query image.
        """
        return self._search(
            query_image=query_image,
            index=self.prototype_index,
            image_paths=self.prototype_paths,
            top_k=top_k,
        )


class GoldProductSearch(BidirectionalJewelrySearch):
    """
    Backward-compatible search class.
    """

    def search(
        self, query_image: Image.Image, top_k: int = TOP_K
    ) -> List[Dict[str, Any]]:
        return self.search_gold(query_image, top_k=top_k)