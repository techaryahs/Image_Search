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

from src.model import DINOv2Encoder


class BidirectionalJewelrySearch:

    # ======================================================
    # VALID / INVALID IMAGE THRESHOLD
    # ======================================================
    #
    # This is an initial testing threshold.
    # It should be tuned later using valid and invalid images.
    #
    MATCH_THRESHOLD = 0.03

    def __init__(
        self,
        encoder: DINOv2Encoder = None
    ):

        print(
            "Loading Bidirectional Jewelry Search Engine..."
        )

        self.encoder = (
            encoder
            if encoder is not None
            else DINOv2Encoder()
        )

        self.load_indexes()

    # ======================================================
    # LOAD INDEXES
    # ======================================================

    def load_indexes(self):

        # ==================================================
        # GOLD INDEX
        # ==================================================

        if (
            GOLD_INDEX_FILE.exists()
            and GOLD_PATHS_FILE.exists()
        ):

            self.gold_index = faiss.read_index(
                str(GOLD_INDEX_FILE)
            )

            self.gold_paths = np.load(
                GOLD_PATHS_FILE,
                allow_pickle=True
            )

            print(
                f"Loaded Gold index with "
                f"{self.gold_index.ntotal} products."
            )

        else:

            self.gold_index = None
            self.gold_paths = np.array([])

            print(
                "Gold index file not found."
            )

        # ==================================================
        # PROTOTYPE INDEX
        # ==================================================

        if (
            PROTOTYPE_INDEX_FILE.exists()
            and PROTOTYPE_PATHS_FILE.exists()
        ):

            self.prototype_index = faiss.read_index(
                str(PROTOTYPE_INDEX_FILE)
            )

            self.prototype_paths = np.load(
                PROTOTYPE_PATHS_FILE,
                allow_pickle=True
            )

            print(
                f"Loaded Prototype index with "
                f"{self.prototype_index.ntotal} prototypes."
            )

        else:

            self.prototype_index = None
            self.prototype_paths = np.array([])

            print(
                "Prototype index file not found."
            )

    # ======================================================
    # GET IMAGE EMBEDDING
    # ======================================================

    def _get_embedding(
        self,
        image: Image.Image
    ) -> np.ndarray:

        embedding = self.encoder.encode_image(
            image
        )

        embedding = np.asarray(
            embedding,
            dtype=np.float32
        )

        embedding = embedding.reshape(
            1,
            -1
        )

        faiss.normalize_L2(
            embedding
        )

        return embedding

    # ======================================================
    # NORMAL SEARCH
    # ======================================================

    def _search(
        self,
        query_image: Image.Image,
        index: faiss.Index,
        image_paths: np.ndarray,
        top_k: int = TOP_K,
    ) -> List[Dict[str, Any]]:

        if (
            index is None
            or len(image_paths) == 0
        ):
            return []

        query_embedding = self._get_embedding(
            query_image
        )

        actual_k = min(
            top_k,
            index.ntotal
        )

        if actual_k <= 0:
            return []

        scores, indices = index.search(
            query_embedding,
            actual_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx == -1:
                continue

            results.append(
                {
                    "image_path": str(
                        image_paths[idx]
                    ),
                    "similarity": float(score),
                }
            )

        return results

    # ======================================================
    # PROTOTYPE → GOLD
    # ======================================================

    def search_gold(
        self,
        query_image: Image.Image,
        top_k: int = TOP_K
    ) -> List[Dict[str, Any]]:

        return self._search(
            query_image=query_image,
            index=self.gold_index,
            image_paths=self.gold_paths,
            top_k=top_k,
        )

    # ======================================================
    # GOLD → PROTOTYPE
    # WITH SPECIFICITY RERANKING
    # ======================================================

    def search_prototype(
        self,
        query_image: Image.Image,
        top_k: int = TOP_K
    ) -> List[Dict[str, Any]]:

        if (
            self.prototype_index is None
            or len(self.prototype_paths) == 0
        ):
            return []

        if (
            self.gold_index is None
            or len(self.gold_paths) == 0
        ):
            return self._search(
                query_image=query_image,
                index=self.prototype_index,
                image_paths=self.prototype_paths,
                top_k=top_k,
            )

        # --------------------------------------------------
        # QUERY EMBEDDING
        # --------------------------------------------------

        query_embedding = self._get_embedding(
            query_image
        )

        # --------------------------------------------------
        # DIRECT GOLD → PROTOTYPE SIMILARITY
        # --------------------------------------------------

        prototype_count = (
            self.prototype_index.ntotal
        )

        direct_scores, prototype_indices = (
            self.prototype_index.search(
                query_embedding,
                prototype_count
            )
        )

        reranked_results = []

        # --------------------------------------------------
        # SPECIFICITY RERANKING
        # --------------------------------------------------

        for direct_score, prototype_idx in zip(
            direct_scores[0],
            prototype_indices[0]
        ):

            if prototype_idx == -1:
                continue

            # Get prototype embedding
            prototype_vector = (
                self.prototype_index.reconstruct(
                    int(prototype_idx)
                )
            )

            prototype_vector = np.asarray(
                prototype_vector,
                dtype=np.float32
            ).reshape(
                1,
                -1
            )

            faiss.normalize_L2(
                prototype_vector
            )

            # Compare this prototype with ALL Gold images
            gold_scores, _ = self.gold_index.search(
                prototype_vector,
                self.gold_index.ntotal
            )

            all_gold_scores = gold_scores[0]

            # --------------------------------------------------
            # Find second strongest Gold similarity.
            #
            # If a prototype matches many Gold images strongly,
            # it behaves like a generic / ambiguous prototype.
            # --------------------------------------------------

            if len(all_gold_scores) > 1:

                second_best_gold_score = float(
                    all_gold_scores[1]
                )

            else:

                second_best_gold_score = 0.0

            direct_score = float(
                direct_score
            )

            # --------------------------------------------------
            # SPECIFICITY SCORE
            # --------------------------------------------------

            specificity_score = (
                direct_score
                - second_best_gold_score
            )

            reranked_results.append(
                {
                    "image_path": str(
                        self.prototype_paths[
                            prototype_idx
                        ]
                    ),
                    "similarity": direct_score,
                    "specificity": specificity_score,
                }
            )

        # --------------------------------------------------
        # SORT BY SPECIFICITY
        # --------------------------------------------------

        reranked_results.sort(
            key=lambda x: x["specificity"],
            reverse=True
        )

        # --------------------------------------------------
        # FINAL RESULTS
        # --------------------------------------------------

        results = []

        for item in reranked_results[:top_k]:

            results.append(
                {
                    "image_path": item[
                        "image_path"
                    ],

                    "similarity": item[
                        "similarity"
                    ],

                    "specificity": item[
                        "specificity"
                    ],
                }
            )

        return results

    # ======================================================
    # VALID / INVALID IMAGE CHECK
    # ======================================================

    def check_image_validity(
        self,
        query_image: Image.Image
    ) -> Dict[str, Any]:

        # --------------------------------------------------
        # Prototype index check
        # --------------------------------------------------

        if (
            self.prototype_index is None
            or self.prototype_index.ntotal == 0
        ):

            return {
                "valid": False,
                "message": (
                    "Invalid Image - "
                    "Prototype index not available."
                ),
                "best_match": None,
                "similarity": 0.0,
            }

        # --------------------------------------------------
        # Create query embedding
        # --------------------------------------------------

        query_embedding = self._get_embedding(
            query_image
        )

        # --------------------------------------------------
        # Search all prototypes
        # --------------------------------------------------

        scores, indices = (
            self.prototype_index.search(
                query_embedding,
                self.prototype_index.ntotal
            )
        )

        # --------------------------------------------------
        # No result
        # --------------------------------------------------

        if len(scores[0]) == 0:

            return {
                "valid": False,
                "message": (
                    "Invalid Image - "
                    "No reliable match found."
                ),
                "best_match": None,
                "similarity": 0.0,
            }

        # --------------------------------------------------
        # Best raw similarity
        # --------------------------------------------------

        best_score = float(
            scores[0][0]
        )

        best_index = int(
            indices[0][0]
        )

        # --------------------------------------------------
        # Invalid FAISS index
        # --------------------------------------------------

        if best_index == -1:

            return {
                "valid": False,
                "message": (
                    "Invalid Image - "
                    "No reliable match found."
                ),
                "best_match": None,
                "similarity": 0.0,
            }

        # --------------------------------------------------
        # Best matching prototype
        # --------------------------------------------------

        best_match = str(
            self.prototype_paths[
                best_index
            ]
        )

        # --------------------------------------------------
        # THRESHOLD CHECK
        # --------------------------------------------------

        is_valid = (
            best_score >= self.MATCH_THRESHOLD
        )

        if is_valid:

            message = "Valid Image"

        else:

            message = (
                "Invalid Image - "
                "No reliable match found."
            )

        return {
            "valid": is_valid,
            "message": message,
            "best_match": best_match,
            "similarity": best_score,
            "threshold": self.MATCH_THRESHOLD,
        }


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

class GoldProductSearch(
    BidirectionalJewelrySearch
):

    """
    Backward-compatible search class.
    """

    def search(
        self,
        query_image: Image.Image,
        top_k: int = TOP_K
    ) -> List[Dict[str, Any]]:

        return self.search_gold(
            query_image,
            top_k=top_k
        )